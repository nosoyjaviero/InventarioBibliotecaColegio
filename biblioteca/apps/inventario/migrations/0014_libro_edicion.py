# Generated by Django 4.1.7 on 2023-06-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0013_alter_libro_fecha_publicacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='edicion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
