from django.contrib import admin
from .models import Ejemplar,Libro,Multa,Prestamo,Usuario
# Register your models here.

admin.site.register(Ejemplar)
admin.site.register(Libro)
admin.site.register(Multa)
admin.site.register(Prestamo)
admin.site.register(Usuario)