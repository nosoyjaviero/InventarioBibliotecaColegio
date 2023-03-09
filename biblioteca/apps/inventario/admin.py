from django.contrib import admin
from .models import Ejemplar,Libro,Multa,Prestamo,Usuario
# Register your models here.

admin.site.register(Ejemplar)
admin.site.register(Libro)
admin.site.register(Multa)
# admin.site.register(Prestamo)
admin.site.register(Usuario)

class PrestamoAdmin(admin.ModelAdmin):
    list_display=(      
         
        'usuario',
        'ejemplar',
        'fecha_prestamo',
        'fecha_devolucion',
        'devuelto',       
         
    )
    
    # search_fields=('ejemplar',)    
    list_filter=('ejemplar', 'fecha_devolucion') 
  
 
admin.site.register(Prestamo, PrestamoAdmin)

