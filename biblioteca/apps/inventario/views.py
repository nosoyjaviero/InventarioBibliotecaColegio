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

from .forms import PrestamoForm, EjemplarForm

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
    """La función select_usuarios renderiza la plantilla 'inventario/crear/prueba2.html' y pasa como contexto un diccionario con los objetos Usuario obtenidos desde la base de datos.Estas líneas de código corresponden a la función select_usuarios, que recibe una solicitud request como argumento y devuelve una respuesta HTTP que renderiza una plantilla HTML.

    En la primera línea, se está declarando la variable usuarios que contiene todos los objetos de Usuario almacenados en la base de datos, utilizando el método all() de la clase Usuario.

    En la segunda línea, se está utilizando la función render de Django para crear una respuesta HTTP que renderiza una plantilla HTML llamada prueba2.html, ubicada en la carpeta inventario/crear.

    Finalmente, se está pasando un diccionario como tercer argumento a render, que contiene dos claves: modelo_usuario y usuarios. La clave modelo_usuario tiene como valor la clase Usuario, mientras que la clave usuarios tiene como valor la variable usuarios creada anteriormente. Esta información se utiliza dentro de la plantilla HTML para mostrar los usuarios disponibles en la base de datos.

    Args:
    request (HttpRequest): Objeto HttpRequest que contiene información acerca de la solicitud HTTP actual.

    Returns:
    HttpResponse: Objeto HttpResponse que contiene la respuesta HTTP resultante de la renderización de la plantilla. El contexto incluye el modelo de Usuario y los objetos Usuario obtenidos desde la base de datos.
    """
    usuarios = Usuario.objects.all()
    return render(request, 'inventario/crear/prueba2.html', {'modelo_usuario': Usuario, 'usuarios': usuarios})

def usuarios_por_seccion(request, seccion):
    """Devuelve una respuesta HTTP en formato JSON que contiene los usuarios que pertenecen a una sección específica.
    

    Args:
        request (HttpRequest): El objeto HttpRequest que representa la solicitud HTTP recibida.
        seccion (str): El nombre de la sección para la que se desea recuperar los usuarios.

    Returns:
        JsonResponse: Una respuesta HTTP en formato JSON que contiene una lista de diccionarios, cada uno de los cuales representa un usuario y contiene las claves 'id', 'nombre' y 'apellido'.
    """
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
            ejemplar__libro__titulo__icontains=palabra_clave
            )       
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
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        return self.model.objects.get(pk=pk)

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
    def form_invalid(self, form):
        print(True)
        return super().form_invalid(form)
    
class EjemplarCreateView(CreateView):
    model = Ejemplar
    form_class = EjemplarForm
    template_name = "inventario/crear/crear_ejemplar.html"
    success_url = reverse_lazy('app_inventario:inicio')
    
    def form_valid(self, form):
        libro_id = form.cleaned_data['libro_id']
        try:
            libro = Libro.objects.get(id=libro_id)
        except Libro.DoesNotExist:
            form.add_error('libro_id', 'No existe usuario con este ID')
            return super().form_invalid(form)
        
        ejemplar = form.save(commit=False)
        ejemplar.libro = libro
        ejemplar.save()
        
        return super().form_valid(form)
    
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
        # Obtener la cédula del usuario y comprobar si existe
        cedula_usuario = form.cleaned_data['cedula_usuario']
        usuario = None
        try:
            usuario = Usuario.objects.get(cedula=cedula_usuario)
        except Usuario.DoesNotExist:
            form.add_error('cedula_usuario', 'No existe usuario con esta cédula')

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
    """La función cargar_libros permite importar una lista de libros desde un archivo CSV en la base de datos. Si el método de la solicitud es POST, se lee el archivo CSV, se itera sobre las filas y se crea o se actualiza cada libro en la base de datos. Si el libro ya existe en la base de datos, se agrega su título a una lista de libros no importados. Finalmente, se devuelve un mensaje indicando si todos los libros se importaron correctamente o si algunos no se importaron porque ya existían en la base de datos. Si el método de solicitud no es POST, se devuelve la página de carga de libros.

    Args:
        El parámetro "request" es un objeto HttpRequest que contiene información sobre la solicitud HTTP actual.

    Returns:
        La función cargar_libros, la sección "Returns" no describe el valor de retorno de la función, por lo que debería ser completada con la información adecuada. Por lo general, el valor de retorno en una función en Django suele ser un objeto HttpResponse
    """
    #la solicitud es una solicitud POST.
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
    """Permite importar un archivo CSV con información de usuarios y agregarlos a la base de datos. La función cargar_usuarios permite importar un archivo CSV con información de usuarios y agregarlos a la base de datos. Si el archivo es cargado correctamente, los datos son procesados línea por línea para crear nuevos objetos de Usuario con los campos especificados. Si el usuario ya existe en la base de datos, la información no será importada y su cédula será registrada en una lista de usuarios no importados.

    Finalmente, la función devuelve una respuesta HttpResponse que renderiza una plantilla HTML, que puede incluir un mensaje indicando cuántos usuarios se importaron correctamente y cuáles no. Si la petición HTTP no es una petición POST, se renderiza la plantilla HTML vacía para permitir la carga del archivo CSV.

    Args:
        request (HttpRequest): La petición HTTP recibida por la vista.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla HTML de importación de usuarios.
    """
    if request.method == 'POST':
        
        #Esta línea asigna a la variable archivo el archivo enviado mediante una solicitud POST en el campo 'csv_file'.
        archivo = request.FILES['csv_file']
        
        #Lee el contenido del archivo asignado a la variable archivo, decodifica los bytes a formato UTF-8 y divide el contenido en líneas, lo que devuelve una lista de cadenas.
        datos_csv = archivo.read().decode('utf-8').splitlines()
        
        #Crea un objeto csv.DictReader que toma una secuencia de líneas (en este caso, datos_csv) y devuelve un iterador que produce diccionarios por cada línea, usando la primera línea como encabezado.
        lector_csv = csv.DictReader(datos_csv)
        
        #Crea una lista vacía llamada 
        usuarios_no_importados = []


        for linea in lector_csv:
            #se utiliza para obtener el valor de la columna "cedula" de la línea actual del archivo CSV.         
            cedula = linea["cedula"]
            
            #se utiliza para crear un nuevo objeto Usuario en la base de datos con los valores de nombre, apellido, cedula, direccion, telefono, correo_electronico y seccion correspondientes a la línea actual del archivo CSV. Si ya existe un objeto Usuario con el mismo valor de cedula en la base de datos, se devuelve ese objeto en lugar de crear uno nuevo.
            #La variable creado se utiliza para indicar si se creó un nuevo objeto Usuario o si se recuperó uno existente de la base de datos.
            usuario, creado = Usuario.objects.get_or_create(
                    nombre=linea["nombre"],
                    apellido=linea["apellido"],
                    cedula=cedula,
                    direccion=linea["direccion"],
                    telefono=linea["telefono"],
                    correo_electronico=linea["correo_electronico"],
                    seccion=linea["seccion"],
                )
            
            #Si no se creó un nuevo objeto Usuario en la línea actual del archivo CSV porque ya existía uno con el mismo valor de cedula, se agrega el valor de cedula a la lista usuarios_no_importados
            if not creado:
                
                #Al final del bucle, la lista usuarios_no_importados contiene las cedulas de los usuarios que no se pudieron importar porque ya existían en la base de datos.
                usuarios_no_importados.append(cedula)

        #Estas líneas de código se encargan de mostrar un mensaje de éxito o de error en la importación de los usuarios desde un archivo CSV. Si se encontraron usuarios que ya existen en la base de datos, se agregan sus cédulas a una lista llamada usuarios_no_importados. Luego, si esa lista no está vacía, se construye un mensaje de error que incluye las cédulas de los usuarios que no se importaron debido a que ya existen en la base de datos. Si la lista está vacía, significa que todos los usuarios se importaron correctamente, por lo que se construye un mensaje de éxito. Finalmente, se renderiza un template HTML que muestra el mensaje.
        if usuarios_no_importados:
            mensaje = f"Los siguientes usuarios no se importaron porque ya existen en la base de datos: {', '.join(usuarios_no_importados)}"
        else:
            mensaje = "Todos los usuarios se importaron correctamente."
        return render(request, 'inventario/crear/rellenar_usuarios.html', {'mensaje': mensaje})
    
    # Si la petición HTTP no es POST, renderizar la plantilla vacía
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
    """
    Vista de lista que muestra una lista paginada de usuarios que coinciden con la palabra clave de búsqueda.

    Args:
        ListView (tipo): Clase base de vista genérica para mostrar una lista de objetos.

    Returns:
        tipo: Una lista paginada de objetos de Usuario ordenados por seccion, que coinciden con la palabra clave de búsqueda.
    """
    template_name= 'inventario/listar/listar_usuarios.html'
    paginate_by=30
    ordering='seccion'    
    
    def get_queryset(self):
        """
        Devuelve la lista paginada de usuarios que coinciden con la palabra clave de búsqueda.

        Returns:
            lista: Una lista paginada de objetos de Usuario que coinciden con la palabra clave de búsqueda.
        """
        palabra_clave= self.request.GET.get("kword", '') #'
        lista= Usuario.objects.filter(
            Q(nombre__icontains=palabra_clave) |Q(apellido__icontains=palabra_clave)
        )
        
        
        return lista