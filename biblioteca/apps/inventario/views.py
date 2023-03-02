from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse

from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from .models import Libro, Prestamo


from django.views.generic import (
     ListView,
    DetailView,
    CreateView,
    TemplateView,
    UpdateView, 
    DeleteView
    )
# Create your views here.

# class InicioView(TemplateView):
#     template_name= 'inicio.html'

class Inicio(ListView):
    template_name= 'inicio.html'
    model=Libro
    context_object_name= 'libros'
    
class ListaDeLibros(ListView):
    template_name= 'inventario/libros.html'
    model=Libro
    context_object_name= 'libros'
    
class DetalleLibro(DetailView):
    template_name= 'inventario/libro.html'
    model=Libro
    context_object_name= 'libro'


class PrestamosVencidos(ListView):
    model = Prestamo
    template_name = 'inventario/prestamos_vencidos.html'

    def get_queryset(self):
        hoy = timezone.now().date()
        dias_atras = hoy - timedelta(days=15)
        queryset = Prestamo.objects.filter(fecha_prestamo__lte=dias_atras, devuelto=False)
        return queryset
    
    