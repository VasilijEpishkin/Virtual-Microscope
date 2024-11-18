from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from pathlib import Path
from .utils import ImageProcessor
import os
from django.core.exceptions import ValidationError


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.svs', '.ndpi', '.tif', '.png', '.jpg', '.jpeg']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions are: ' + ', '.join(valid_extensions))

class TiledImage(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    original_image = models.FileField(
    upload_to='originals/',
    validators=[validate_image_extension]
)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Поля для тайлов
    tile_size = models.IntegerField(
        default=256,
        validators=[MinValueValidator(1)],
        help_text="Размер тайла в пикселях"
    )
    zoom_levels = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Количество уровней масштабирования"
    )
    width = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Ширина оригинального изображения",
        null=True,
        blank=True,
    )
    height = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Высота оригинального изображения",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def get_tile_path(self, zoom, x, y):
        return f'tiles/{self.id}/zoom_{zoom}/{x}_{y}.png'

    def process_image(self):
        if not self.original_image:
            raise ValueError("Изображение не загружено")
            
        processor = ImageProcessor(
            self.original_image.path,
            settings.MEDIA_ROOT,
            self.tile_size
        )
        
        result = processor.create_tiles(self.id)
        
        self.zoom_levels = result['zoom_levels']
        self.width = result['width']
        self.height = result['height']
        self.save()

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        
        if is_new and self.original_image:
            self.process_image()

    class Meta:
        verbose_name = "Тайловое изображение"
        verbose_name_plural = "Тайловые изображения"