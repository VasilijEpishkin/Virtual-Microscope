# Generated by Django 4.2.16 on 2024-11-15 13:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiles', '0003_alter_tiledimage_original_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiledimage',
            name='height',
            field=models.IntegerField(blank=True, help_text='Высота оригинального изображения', null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='tiledimage',
            name='width',
            field=models.IntegerField(blank=True, help_text='Ширина оригинального изображения', null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]