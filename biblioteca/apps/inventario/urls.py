
from django.urls import path
from . import views

app_name= 'app_inventario'
urlpatterns = [
    path( '', views.PrestamosVencidos.as_view(), name='inicio'),
    path('libros/', views.ListaDeLibros.as_view() , name='libros'),
    path('libro/<pk>', views.DetalleLibro.as_view(), name='libro'),
    # path('new-departamento/', views.NewDepartamientoView.as_view(), name='nuevo_departamento'),
    # path('departamento-lista/', views.DepartamentoListView.as_view(), name='list_departamento'),
]
