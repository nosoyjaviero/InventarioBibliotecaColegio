
from django.urls import path
from . import views

app_name= 'app_inventario'
urlpatterns = [
   
    path( '', views.Inicio.as_view(), name='inicio'),
    path('libros/', views.ListaDeLibros.as_view() , name='libros'),
    path('libro/<pk>', views.DetalleLibro.as_view(), name='libro'),
    
    path('editar-libro/<pk>', views.EditarLibro.as_view(), name='editar_libro'), 
    
    #ejemplares
    path('editar-ejemplar/<pk>', views.EditarEjemplar.as_view(), name='editar_ejemplar'),
    path('ejemplares', views.ListaDeEjemplares.as_view(), name='ejemplares'),
     
   # usuario
   path('cargar_usuario', views.cargar_usuarios, name="cargar_usuarios"),
   path('cargar_libro', views.cargar_libros, name="cargar_libros"),
   
   
    path('prueba/', views.Secciones, name='prueba'),
   #  path('otra_vista/<seccion_id>/', views.SeleccionarUsuario, name='otra_vista'),
   #  path('usuarios/por_seccion/<str:seccion>/', views.UsuarioPorSeccionListView.as_view(), name='usuarios_por_seccion'),
   
       path('prestamo/crear/', views.PrestamoCreateView.as_view(), name='crear_prestamo'),
    path('usuario/buscar/', views.UsuarioSearchView.as_view(), name='buscar_usuario'),
    path('prueba2', views.select_usuarios, name='prueba2'),
  path('usuarios/<str:seccion>/', views.usuarios_por_seccion, name='usuarios_por_seccion'),
       
       
   path('devolver-prestamo/<pk>/', views.DevolverPrestamo.as_view(), name='devolver_ejemplar'),
   path('fecha/<pk>/', views.ActualizarFechaPrestamo.as_view(), name='actualizar_fecha'),
       

    #    Crear
       path('crear-libro/', views.LibroCreateView.as_view(), name='registrar_libro'),
       
       
       path('crear-Usuario/', views.UsuarioCreateView.as_view(), name='registrar_usuario'),
       
       path('crear-Ejemplar/', views.EjemplarCreateView.as_view(), name='registrar_ejemplar'),
       
       path('registrar-Multa/', views.MultaCreateView.as_view(), name='registrar_multa'),
       
       path('registrar-Prestamo/', views.PrestamoCreateView.as_view(), name='registrar_prestamo'),
    #   Fin Crear
   
   
   #listar
    path('prestamos/', views.libros_prestados.as_view(), name='prestamos'),
    path('prestamos-vencidos/', views.PrestamosVencidos.as_view(), name='prestamos-vencidos'),
    
    
   #  usuarios
    path('listar-usuarios/', views.ListarUsuarios.as_view(), name='lista_usuarios'),
    path('editar-usuario/<pk>', views.EditarUsuario.as_view(), name='editar_usuario'),
    
    path('elimina-usuarior/<pk>', views.UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('eliminar-libro/<pk>', views.LibroDeleteView.as_view(), name='eliminar_libro'),
    path('eliminar-ejemplar/<pk>', views.EjemplaresDeleteView.as_view(), name='eliminar_ejemplar'),
    
    
   #fin listar
   
]
