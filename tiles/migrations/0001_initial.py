# Generated by Django 4.2.16 on 2024-11-15 11:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TiledImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('original_image', models.ImageField(upload_to='originals/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tile_size', models.IntegerField(default=256, help_text='Размер тайла в пикселях', validators=[django.core.validators.MinValueValidator(1)])),
                ('zoom_levels', models.IntegerField(default=1, help_text='Количество уровней масштабирования', validators=[django.core.validators.MinValueValidator(1)])),
                ('tiles_folder', models.CharField(blank=True, help_text='Путь к папке с тайлами', max_length=255)),
                ('width', models.IntegerField(help_text='Ширина оригинального изображения', null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('height', models.IntegerField(help_text='Высота оригинального изображения', null=True, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'Тайловое изображение',
                'verbose_name_plural': 'Тайловые изображения',
            },
        ),
    ]
