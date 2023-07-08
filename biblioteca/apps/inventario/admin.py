from django.contrib import admin
from .models import Ejemplar,Libro,Prestamo,Usuario
# Register your models here.

admin.site.register(Ejemplar)
admin.site.register(Libro)
# admin.site.register(Prestamo)


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


class UsuarioAdmin(admin.ModelAdmin):
    list_display=( 
        'cedula',     
         'nombre',    
        'apellido',        
        'direccion',
        'telefono',   
        'correo_electronico',   
        'seccion',
    
         
               
         
    )
    
    search_fields=('cedula','nombre','seccion',)    
    list_filter=('nombre', 'cedula') 
    
    
admin.site.register(Usuario, UsuarioAdmin)
