from django.contrib import admin
from .models import TiledImage

@admin.register(TiledImage)
class TiledImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'tile_size', 'zoom_levels', 'width', 'height')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')