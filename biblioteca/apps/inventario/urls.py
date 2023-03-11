
from django.urls import path
from . import views

app_name= 'app_inventario'
urlpatterns = [
   
    path( '', views.Inicio.as_view(), name='inicio'),
    path('libros/', views.ListaDeLibros.as_view() , name='libros'),
    path('libro/<pk>', views.DetalleLibro.as_view(), name='libro'),
    
    path('editar-libro/<pk>', views.EditarLibro.as_view(), name='editar_libro'), 
    
    path('editar-ejemplar/<pk>', views.EditarEjemplar.as_view(), name='editar_ejemplar'),
    
    
    path('ejemplares', views.ListaDeEjemplares.as_view(), name='ejemplares'),
     
   path('cargar_usuario', views.cargar_usuarios, name="cargar_usuarios"),
   path('cargar_libro', views.cargar_libros, name="cargar_libros"),
   
   
    path('prueba/', views.Secciones, name='prueba'),
    path('otra_vista/<seccion_id>/', views.SeleccionarUsuario, name='otra_vista'),
       
       
   path('prestamo/<pk>/', views.DevolverPrestamo.as_view(), name='devolver_ejemplar'),
   path('fecha/<pk>/', views.ActualizarFechaPrestamo.as_view(), name='actualizar_fecha'),
       
       
    #    Crear
       path('registrar-Libro/', views.LibroCreateView.as_view(), name='registrar_libro'),
       
       path('registrar-Usuario/', views.UsuarioCreateView.as_view(), name='registrar_usuario'),
       
       path('registrar-Ejemplar/', views.EjemplarCreateView.as_view(), name='registrar_ejemplar'),
       
       path('registrar-Multa/', views.MultaCreateView.as_view(), name='registrar_multa'),
       
       path('registrar-Prestamo/', views.PrestamoCreateView.as_view(), name='registrar_prestamo'),
    #   Fin CrearCrear
   
   
   #listar
    path('prestamos/', views.libros_prestados.as_view(), name='prestamos'),
    path('prestamos-vencidos/', views.PrestamosVencidos.as_view(), name='prestamos-vencidos'),
   #fin listar
]
