# Generated by Django 4.1.7 on 2023-07-07 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0022_remove_ejemplar_ubicacion'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Multa',
        ),
    ]