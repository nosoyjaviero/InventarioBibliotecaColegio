# Generated by Django 4.1.7 on 2023-06-24 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0021_remove_ejemplar_comentarios_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ejemplar',
            name='ubicacion',
        ),
    ]
