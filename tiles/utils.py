import openslide
from PIL import Image
import os
from pathlib import Path
import math

class ImageProcessor:
    def __init__(self, image_path, output_base_dir, tile_size=256):
        self.image_path = image_path
        ext = os.path.splitext(image_path)[1].lower()
        
        if ext == '.svs':
            self.slide = openslide.OpenSlide(image_path)
            self.width, self.height = self.slide.dimensions
            self.is_svs = True
        else:
            self.image = Image.open(image_path)
            self.width, self.height = self.image.size
            self.is_svs = False
            
        self.tile_size = tile_size
        self.output_base_dir = Path(output_base_dir)

    def get_tile(self, x, y, level_width, level_height, scale):
        if self.is_svs:
            region = self.slide.read_region(
                (x * self.tile_size * scale, y * self.tile_size * scale),
                0,
                (self.tile_size, self.tile_size)
            )
            return region.convert('RGB')
        else:
            right = min(x + self.tile_size, level_width)
            bottom = min(y + self.tile_size, level_height)
            return self.image.crop((x, y, right, bottom))

    def create_tiles(self, image_id):
        zoom_levels = math.ceil(math.log2(max(self.width, self.height) / self.tile_size))
        tiles_dir = self.output_base_dir / f'tiles/{image_id}'
        tiles_dir.mkdir(parents=True, exist_ok=True)

        for zoom in range(zoom_levels):
            scale = 2 ** (zoom_levels - zoom - 1)
            level_width = self.width // scale
            level_height = self.height // scale
            
            zoom_dir = tiles_dir / f'zoom_{zoom}'
            zoom_dir.mkdir(exist_ok=True)

            for y in range(0, level_height, self.tile_size):
                for x in range(0, level_width, self.tile_size):
                    tile = self.get_tile(x, y, level_width, level_height, scale)
                    
                    if tile.size != (self.tile_size, self.tile_size):
                        new_tile = Image.new('RGB', (self.tile_size, self.tile_size), 'white')
                        new_tile.paste(tile, (0, 0))
                        tile = new_tile

                    tile_x = x // self.tile_size
                    tile_y = y // self.tile_size
                    tile.save(zoom_dir / f'{tile_x}_{tile_y}.png')

        if self.is_svs:
            self.slide.close()

        return {
            'zoom_levels': zoom_levels,
            'width': self.width,
            'height': self.height
        }