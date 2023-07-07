
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.auth.decorators import login_required
from . import views

app_name= 'app_inventario'
urlpatterns = [
   
    path('', views.Inicio.as_view(), name='inicio'),
    
    #libro
    path('libros/', views.ListaDeLibros.as_view() , name='libros'),
    path('libro/<pk>', views.DetalleLibro.as_view(), name='libro'),    
    path('cargar_libro', views.cargar_libros, name="cargar_libros"),  
    path('crear-libro/', views.LibroCreateView.as_view(), name='registrar_libro'),       
    path('editar-libro/<pk>', views.EditarLibro.as_view(), name='editar_libro'),     
    path('eliminar-libro/<pk>', views.LibroDeleteView.as_view(), name='eliminar_libro'),
    
    #ejemplares
    
    path('crear-Ejemplar/', views.EjemplarCreateView.as_view(), name='registrar_ejemplar'),
    path('editar-ejemplar/<pk>', views.EditarEjemplar.as_view(), name='editar_ejemplar'),
    path('ejemplares', views.ListaDeEjemplares.as_view(), name='ejemplares'),    
    path('eliminar-ejemplar/<pk>', views.EjemplaresDeleteView.as_view(), name='eliminar_ejemplar'),
     
   # usuario
   
    path('crear-Usuario/', views.UsuarioCreateView.as_view(), name='registrar_usuario'),
    path('cargar_usuario', views.cargar_usuarios, name="cargar_usuarios"), 
    path('listar-usuarios/', views.ListarUsuarios.as_view(), name='lista_usuarios'),
    path('elimina-usuarior/<pk>', views.UsuarioDeleteView.as_view(), name='eliminar_usuario'),   
    path('usuario/buscar/', views.UsuarioSearchView.as_view(), name='buscar_usuario'),
    path('usuarios/<str:seccion>/', views.usuarios_por_seccion, name='usuarios_por_seccion'),
   
   #  path('otra_vista/<seccion_id>/', views.SeleccionarUsuario, name='otra_vista'),
   #  path('usuarios/por_seccion/<str:seccion>/', views.UsuarioPorSeccionListView.as_view(), name='usuarios_por_seccion'),
   
   
   #prestamo
    path('prestamo/crear/', views.PrestamoCreateView.as_view(), name='crear_prestamo'),
    path('prueba2', views.select_usuarios, name='prueba2'),              
    path('devolver-prestamo/<pk>/', views.DevolverPrestamo.as_view(), name='devolver_ejemplar'),    
    path('fecha/<pk>/', views.ActualizarFechaPrestamo.as_view(), name='actualizar_fecha'),       
    path('registrar-Prestamo/', views.PrestamoCreateView.as_view(), name='registrar_prestamo'),   
    path('prestamos/', views.libros_prestados.as_view(), name='prestamos'),
    path('prestamos-vencidos/', views.PrestamosVencidos.as_view(), name='prestamos-vencidos'),

    
   #  usuarios
    path('editar-usuario/<pk>', views.EditarUsuario.as_view(), name='editar_usuario'),    
    
    
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='app_inventario:inicio'), name='logout'),
   
   
   
]
