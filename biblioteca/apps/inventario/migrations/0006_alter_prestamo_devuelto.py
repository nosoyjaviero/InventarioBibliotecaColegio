# Generated by Django 4.1.7 on 2023-03-02 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_prestamo_devuelto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='devuelto',
            field=models.BooleanField(blank=True, choices=[(True, 'Si'), (False, 'No')], max_length=10, null=True),
        ),
    ]