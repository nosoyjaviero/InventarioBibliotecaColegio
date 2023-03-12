from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect

from django.urls import reverse_lazy,reverse
from django.contrib import messages

from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from datetime import date
from datetime import timedelta
import csv
from functools import partial

from .forms import PrestamoForm

from .models import Libro, Prestamo, Usuario, Ejemplar,Multa

from django.views.generic.edit import FormMixin
from django.views.generic import (
    View,
     ListView,
    DetailView,
    CreateView,
    TemplateView,
    UpdateView, 
    DeleteView
    )
# Create your views here.

def select_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'inventario/crear/prueba2.html', {'modelo_usuario': Usuario, 'usuarios': usuarios})

def usuarios_por_seccion(request, seccion):
    usuarios = Usuario.objects.filter(seccion=seccion)
    data = [{'id': usuario.id, 'nombre': usuario.nombre, 'apellido': usuario.apellido} for usuario in usuarios]
    return JsonResponse(data, safe=False)
# class Prueba(CreateView):

# En el ejemplo que has dado, ids = Prestamo.objects.values_list('id', flat=True), se está obteniendo una lista plana de los valores del campo id de todos los objetos en la tabla Prestamo. Es decir, se obtiene una lista de valores enteros en lugar de una lista de tuplas con un solo elemento que contiene un valor entero.

# Usar flat=True puede ser útil cuando se necesita obtener una lista plana de valores para trabajar con ella más fácilmente, sin tener que procesar las tuplas. En este caso, como solo se necesita obtener los valores del campo id, usar flat=True hace que el código sea más eficiente y más fácil de trabajar con los datos obtenidos.


def Secciones(request):
    if request.method == 'POST':
        seccion = request.POST.get('seccion')
        
        assert(seccion, "")
        if seccion is not None and seccion != '':
            print('Entre'+seccion)
            return redirect('app_inventario:otra_vista', seccion_id=seccion)
        else:
            return redirect('app_inventario:otra_vista')
    else:
        secciones = Usuario.objects.values_list('seccion', flat=True).distinct()
        return render(request, 'inventario/crear/crear_ejemplar1.html', {'secciones': secciones})

    
def SeleccionarUsuario(request, seccion_id=None):
    if seccion_id is not None:
        usuarios = Usuario.objects.filter(seccion=seccion_id)
    else:
        usuarios = Usuario.objects.all()
    
    url_prestamo = reverse('app_inventario:registrar_prestamo')
    url_prestamo += f"?seccion={seccion_id}" if seccion_id is not None else ""
    
    return render(request, 'inventario/crear/crear_ejemplar2.html', {'usuarios': usuarios, 'url_prestamo': url_prestamo})


class libros_prestados(ListView):
    template_name= 'inventario/listar/libros_prestados.html'
    # prestamos = Prestamo.objects.filter(devuelto=False)
    context_object_name= 'prestamos'
    paginate_by=6    
    ordering='fecha_devolucion'
    
    
    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '') 
        lista =Prestamo.objects.filter(
            devuelto=False,
            ejemplar__libro__titulo__icontains=palabra_clave)       
        return lista
    
    # def get_queryset(self):
    #     return Prestamo.objects.filter(devuelto=False)               

class Inicio(ListView):
    template_name= 'inicio.html'
    model=Libro
    context_object_name= 'prestamos'
    paginate_by=6
    def get_queryset(self):
        hoy = date.today()
        # prestamos_hoy = Prestamo.objects.filter( devuelto=False)
        # return prestamos_hoy
        palabra_clave = self.request.GET.get("kword", '') 
        lista =Prestamo.objects.filter(
            fecha_devolucion=hoy,
            devuelto=False,
            ejemplar__libro__titulo__icontains=palabra_clave)       
        return lista
   
class ListaDeLibros(ListView):
    template_name= 'inventario/libros.html'
    # model=Libro
    context_object_name= 'libros'
    paginate_by=6
    ordering='titulo'
    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '') 
        lista =Libro.objects.filter(
            titulo__icontains=palabra_clave)       
        return lista
    
class ListaDeEjemplares(ListView):
    template_name= 'inventario/listar/ejemplares.html'
    # model=Ejemplar
    context_object_name= 'ejemplares'
    paginate_by=6
    ordering='libro__titulo'
    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '') 
        lista =Ejemplar.objects.filter(
            libro__titulo__icontains=palabra_clave)       
        return lista
    
class DetalleLibro(DetailView):
    template_name= 'inventario/libro.html'
    model=Libro
    context_object_name= 'libro'

class PrestamosVencidos(ListView):
    model = Prestamo
    template_name = 'inventario/prestamos_vencidos.html'
    paginate_by=6
    def get_queryset(self):
        hoy = timezone.now().date()
        dias_atras = hoy - timedelta(days=15)
        palabra_clave = self.request.GET.get("kword", '') 
        lista =Prestamo.objects.filter(
            fecha_prestamo__lte=dias_atras,
            devuelto=False,
            ejemplar__libro__titulo__icontains=palabra_clave)       
        return lista
    
class DevolverPrestamo(UpdateView):
    template_name = 'inventario/devolucion.html'
    model = Prestamo
    fields=['devuelto']    
    success_url = reverse_lazy('app_inventario:inicio')  
    
    def form_valid(self, form):
        prestamo = form.save(commit=False)        
        if prestamo.devuelto:
            # restar 1 a la cantidad de Ejemplar
            
            ejemplar = prestamo.ejemplar
            
            if (ejemplar.cantidad == 0 and ejemplar.estado=='prestado'):
                print("entre aqui 1")
                ejemplar.cantidad +=1
                ejemplar.estado='disponible'
                ejemplar.save()
                return super().form_valid(form)
            
            if (ejemplar.cantidad >0 and ejemplar.estado=='disponible'): 
                print("entre aqui 1")               
                ejemplar.cantidad +=1
                ejemplar.save()
                return super().form_valid(form)
        else:
            # si no se confirma la devolución, solo guardar el registro de Prestamo
            return super().form_valid(form)
        
        return super().form_valid(form)
      
class ActualizarFechaPrestamo(UpdateView):
    template_name = 'inventario/editar/actualizar_fecha.html'
    model = Prestamo
    fields=['fecha_devolucion']
    # fields=('__all__')  
    success_url = reverse_lazy('app_inventario:inicio')

class EditarLibro(UpdateView):
    template_name = "inventario/editar/editar_libro.html"
    model = Libro
    fields=('__all__')
    success_url = reverse_lazy('app_inventario:inicio')
    
class EditarEjemplar(UpdateView):
    template_name = "inventario/editar/editar_ejemplar.html"
    model = Ejemplar
    fields=('__all__')
    success_url = reverse_lazy('app_inventario:inicio')

class LibroCreateView(CreateView):
    model = Libro
    template_name = "inventario/crear/crear_libro.html"
    fields=('__all__')

    success_url= reverse_lazy('app_inventario:inicio')
    
class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = "inventario/crear/crear_usuario.html"
    fields=('__all__')

    success_url= reverse_lazy('app_inventario:inicio')
    
class EjemplarCreateView(CreateView):
    model = Ejemplar
    template_name = "inventario/crear/crear_ejemplar.html"
    fields=('__all__')

    success_url= reverse_lazy('app_inventario:inicio')
    
class MultaCreateView(CreateView):
    model = Multa
    template_name = "inventario/crear/crear_multa.html"
    fields=('__all__')

    success_url= reverse_lazy('app_inventario:inicio')


class PrestamoCreateView(CreateView, FormMixin):
    template_name = "inventario/crear/crear_prestamo.html"
    form_class = PrestamoForm
    success_url = reverse_lazy('app_inventario:inicio')

    def form_valid(self, form):
        # Obtener el ID del usuario y comprobar si existe
        id_usuario = form.cleaned_data['id_usuario']
        usuario = None
        try:
            usuario = Usuario.objects.get(id=id_usuario)
        except Usuario.DoesNotExist:
            print('No existe usuario con este ID')
            form.add_error('id_usuario', 'No existe usuario con este ID')

        # Obtener el ID del ejemplar y comprobar si existe y está disponible
        id_ejemplar = form.cleaned_data['id_ejemplar']
        ejemplar = None
        try:
            ejemplar = Ejemplar.objects.get(id=id_ejemplar, estado='disponible')
        except Ejemplar.DoesNotExist:
            print('No existe ejemplar con este ID o no está disponible')
            form.add_error('id_ejemplar', 'No existe ejemplar con este ID o no está disponible')

        # Si el usuario y el ejemplar existen, crear el préstamo
        if usuario and ejemplar:
            form.instance.usuario = usuario
            form.instance.ejemplar = ejemplar

            # Actualizar el estado del ejemplar y la cantidad disponible
            ejemplar.cantidad -= 1
            if ejemplar.cantidad == 0:
                ejemplar.estado = 'prestado'
            ejemplar.save()

            # Continuar con el procesamiento del formulario
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
 
def cargar_libros(request):
    if request.method == 'POST':
        archivo = request.FILES['csv_file']
        datos_csv = archivo.read().decode('utf-8').splitlines()
        lector_csv = csv.DictReader(datos_csv)
        libros_no_importados = []

        for linea in lector_csv:
            titulo = linea["titulo"]
            libro, creado = Libro.objects.get_or_create(
                    titulo=titulo,
                    autor=linea["autor"],
                    isbn=linea["isbn"],
                    editorial=linea["editorial"],
                    fecha_publicacion=linea["fecha_publicacion"],
                    num_paginas=linea["num_paginas"],
                    avatar=linea["avatar"],
                )
            if not creado:
                libros_no_importados.append(titulo)

        if libros_no_importados:
            mensaje = f"Los siguientes libros no se importaron porque ya existen en la base de datos: {', '.join(libros_no_importados)}"
        else:
            mensaje = "Todos los libros se importaron correctamente."
        return render(request, 'inventario/crear/rellenar_libros.html', {'mensaje': mensaje})

    return render(request, 'inventario/crear/rellenar_libros.html')

def cargar_usuarios(request):
    if request.method == 'POST':
        archivo = request.FILES['csv_file']
        datos_csv = archivo.read().decode('utf-8').splitlines()
        lector_csv = csv.DictReader(datos_csv)
        usuarios_no_importados = []

        for linea in lector_csv:
            cedula = linea["cedula"]
            usuario, creado = Usuario.objects.get_or_create(
                    nombre=linea["nombre"],
                    apellido=linea["apellido"],
                    cedula=cedula,
                    direccion=linea["direccion"],
                    telefono=linea["telefono"],
                    correo_electronico=linea["correo_electronico"],
                    seccion=linea["seccion"],
                )
            if not creado:
                usuarios_no_importados.append(cedula)

        if usuarios_no_importados:
            mensaje = f"Los siguientes usuarios no se importaron porque ya existen en la base de datos: {', '.join(usuarios_no_importados)}"
        else:
            mensaje = "Todos los usuarios se importaron correctamente."
        return render(request, 'inventario/crear/rellenar_usuarios.html', {'mensaje': mensaje})

    return render(request, 'inventario/crear/rellenar_usuarios.html')
   
#     model = Prestamo
#     template_name = 'inventario/prestamos_vencidos.html'

#     def get_queryset(self):
#         hoy = timezone.now().date()
#         dias_atras = hoy - timedelta(days=15)
#         dias_atras_exactos = hoy - timedelta(days=15)
#         queryset = Prestamo.objects.filter(fecha_prestamo=dias_atras_exactos, devuelto=False, fecha_devolucion=hoy)
#         return queryset
   
    # Anterior
# class ActualizarPrestamo(UpdateView):
#     template_name = "inventario/devolucion.html"
#     model = Prestamo
#     fields=('__all__')
    
#     success_url= reverse_lazy('app_inventario:inicio')
    
    
#     def post(self, request, *args, **kwargs):
        
#         self.object= self.get_object()
#         print(request.POST)
#         print(request.POST['devuelto'])
#         return super().post(request, *args, **kwargs)
    
    # def form_valid(self, form):   
        
    #      prestamo=form.save(commit=False) 
    #      prestamo.save()   
         
    #      return super(EditarPrestamo ,self ).form_valid(form)    
           
      
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             prestamo = form.save(commit=False)
#             if prestamo.devuelto:
#                 # restar uno a la cantidad de Ejemplar
#                 ejemplar = prestamo.ejemplar
#                 ejemplar.cantidad += 1
#                 ejemplar.save()

#                 # eliminar el registro de Prestamo
#                 prestamo.delete()
                
#                 return HttpResponseRedirect(self.success_url)
        
#         return self.form_invalid(form)
    
# def devolver_libro(request, pk):
#     prestamo = Prestamo.objects.get(id=pk)

#     if request.method == 'POST':
#         if prestamo.devuelto:
#             # Subtract 1 from quantity and delete the loan record
#             ejemplar = prestamo.ejemplar
#             ejemplar.cantidad -= 1
#             ejemplar.save()
#             prestamo.delete()
#             return redirect('app_inventario:inicio')

#         else:
#             # Set devuelto to True if the user confirms the return
#             prestamo.devuelto = True
#             prestamo.save()
#             return redirect('prestamo_detail', prestamo_id=prestamo.id)

#     context = {'prestamo': prestamo}
#     return render(request, 'inventario/devolucion.html', context)






# Este código define una vista en Django llamada devolver_libro que maneja la devolución de un libro prestado por un usuario. La vista toma como parámetro pk, que es la clave principal del registro del préstamo que se va a devolver.

# La primera línea prestamo = Prestamo.objects.get(pk=pk) recupera el objeto del modelo Prestamo correspondiente al ID pk pasado como parámetro.
# La siguiente línea ejemplar = prestamo.ejemplar obtiene el objeto Ejemplar asociado al préstamo.
# Los próximos dos print se utilizan para imprimir el ID del préstamo y la cantidad actual de ejemplares disponibles.
# El siguiente bloque if comprueba si la solicitud es de tipo POST y si el usuario ha seleccionado la opción "devuelto" en el formulario. Si se cumple esta condición, se ejecuta el siguiente bloque de código:
# La línea ejemplar.cantidad += 1 suma uno a la cantidad de ejemplares disponibles.
# La línea ejemplar.save() guarda el nuevo valor en la base de datos.
# La línea prestamo.delete() elimina el registro de préstamo de la base de datos.
# La vista redirige al usuario a la página de inicio.
# Si la solicitud no es de tipo POST o el usuario no ha seleccionado la opción "devuelto", se renderiza la plantilla "inicio.html" con el objeto prestamo pasado como contexto.

# def devolver_libro(request, pk):
#     prestamo = Prestamo.objects.get(pk=pk)
#     print(prestamo.id)
#     ejemplar = prestamo.ejemplar
    
#     form_class = DevolucionLibroForm
    
#     print(ejemplar.cantidad)
#     print(f'request.POST.get("devuelto") {request.POST.get("devuelto")}')
#     if request.method == "POST" and request.POST.get("devuelto") == 'True':
#         # Restar uno a la cantidad de ejemplares disponibles
#         ejemplar.cantidad += 1
#         ejemplar.save()
#         print(ejemplar.cantidad)
#         # Borrar el registro de préstamo
#         prestamo.delete()

#         return redirect("app_inventario:inicio")

#     return render(request, "inventario/devolucion.html", {"prestamo": prestamo})

class UsuarioSearchView(ListView):
    model = Usuario
    template_name = 'inventario/crear/buscar_usuario.html'
    context_object_name = 'usuario_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Usuario.objects.filter(Q(nombre__icontains=query) | Q(apellido__icontains=query))
        return Usuario.objects.none()


class ListarUsuarios(ListView):
    template_name= 'inventario/listar/listar_usuarios.html'
    paginate_by=30
    ordering='seccion'    
    
    def get_queryset(self):
        
        palabra_clave= self.request.GET.get("kword", '') #'
        lista= Usuario.objects.filter(
            nombre__icontains=palabra_clave
        )
        
        
        return lista