from rest_framework import serializers
from .models import TiledImage

class TiledImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiledImage
        fields = [
            'id',
            'name',
            'description',
            'original_image',
            'created_at',
            'tile_size',
            'zoom_levels',
            'tiles_folder',
            'width',
            'height'
        ]
        read_only_fields = ['created_at']