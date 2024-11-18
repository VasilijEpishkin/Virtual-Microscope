from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from PIL import Image
import os
from .models import TiledImage
from .serializers import TiledImageSerializer

class TiledImageViewSet(viewsets.ModelViewSet):
    queryset = TiledImage.objects.all()
    serializer_class = TiledImageSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        self.process_image(instance)

    @action(detail=True, methods=['post'])
    def generate_tiles(self, request, pk=None):
        image = self.get_object()
        self.process_image(image)
        return Response({'status': 'Tiles generated successfully'})

    def process_image(self, image_obj):
        # Open original image
        img = Image.open(image_obj.original_image.path)
        
        # Update image dimensions
        image_obj.width, image_obj.height = img.size
        
        # Create tiles directory
        tiles_dir = f'tiles/{image_obj.id}'
        os.makedirs(os.path.join(settings.MEDIA_ROOT, tiles_dir), exist_ok=True)
        
        # Generate tiles for each zoom level
        for zoom in range(image_obj.zoom_levels):
            zoom_dir = f'{tiles_dir}/zoom_{zoom}'
            os.makedirs(os.path.join(settings.MEDIA_ROOT, zoom_dir), exist_ok=True)
            
            # Calculate dimensions for current zoom level
            scale = 1 / (2 ** zoom)
            level_width = int(image_obj.width * scale)
            level_height = int(image_obj.height * scale)
            
            # Resize image for current zoom level
            level_img = img.resize((level_width, level_height), Image.Resampling.LANCZOS)
            
            # Generate tiles
            for y in range(0, level_height, image_obj.tile_size):
                for x in range(0, level_width, image_obj.tile_size):
                    # Extract and save tile
                    tile = level_img.crop((
                        x, 
                        y, 
                        min(x + image_obj.tile_size, level_width),
                        min(y + image_obj.tile_size, level_height)
                    ))
                    tile_path = f'{zoom_dir}/{x}_{y}.png'
                    tile.save(os.path.join(settings.MEDIA_ROOT, tile_path), 'PNG')
        
        image_obj.tiles_folder = tiles_dir
        image_obj.save()