from django import forms
from .models import Ejemplar, Prestamo, Libro
from django.forms.widgets import TextInput

# class DevolucionLibroForm(forms.ModelForm):
#     class Meta:
#         model = Prestamo
#         fields = ['devuelto']
#         labels = {
#             'devuelto': '¿Desea devolver el libro?',
#         }
        
        
# class CrearPrestamoForm(forms.ModelForm):
#     class Meta:
#         model = Prestamo
#         fields = [field.name for field in Prestamo._meta.fields]
        
#         widgets = {
#             'usuario': forms.TextInput(attrs={'class': 'form-control'}),
#             'ejemplar': forms.TextInput(attrs={'class': 'form-control'}),
#             'fecha_prestamo': forms.TextInput(attrs={'class': 'form-control'}),
#             'fecha_devolucion': forms.TextInput(attrs={'class': 'form-control'}),
#             'devuelto': forms.TextInput(attrs={'class': 'form-control'}),
#         }
    

class PrestamoForm(forms.ModelForm):
    """Este módulo define un formulario de modelo de Django llamado PrestamoForm. El formulario incluye los campos cedula_usuario, id_ejemplar, fecha_prestamo y fecha_devolucion del modelo Prestamo. 

    Args:
    forms (type): El tipo de objeto forms de Django que se utiliza para definir formularios. Los formularios se utilizan para generar formularios HTML automáticamente y manejar su validación en Django. Los formularios de modelo en Django se utilizan para interactuar con modelos de bases de datos.

    """
    cedula_usuario = forms.CharField(label='Cédula Usuario')
    id_ejemplar = forms.CharField(label='ID Ejemplar')

    class Meta:
        model = Prestamo
        fields = ['cedula_usuario', 'id_ejemplar', 'fecha_prestamo', 'fecha_devolucion' ]
        
class EjemplarForm(forms.ModelForm):
    """Este módulo define un formulario de modelo de Django llamado EjemplarForm. El formulario incluye el campo libro_id y los campos adicionales 'estado', 'ubicacion', 'fecha_adquisicion', 'ultima_revision', 'cantidad' y 'comentarios' del modelo Ejemplar.
    
    Args:
        forms (type): El tipo de objeto forms de Django que se utiliza para definir formularios.

    La función clean_libro_id se utiliza para validar el campo libro_id en el formulario. Si no se encuentra un libro con el ID proporcionado en la base de datos, se levantará una excepción forms.ValidationError.

    Raises:
        forms.ValidationError: Si no se encuentra un libro con el ID proporcionado.

    Returns:
        int: El ID del libro proporcionado en el formulario.
    """
    libro_id = forms.IntegerField(label='ID del libro')
    
    class Meta:
        model = Ejemplar
        # fields = ('estado', 'ubicacion',  'ultima_revision', 'cantidad', 'comentarios')
        fields = ('estado', 'isbn',  'ultima_revision', 'cantidad', 'ano_aquision', 'año_publicacion', 'editorial', 'cutter', 'dewey' ,  'edicion')
        
    def clean_libro_id(self):
        libro_id = self.cleaned_data['libro_id']
        try:
            libro = Libro.objects.get(id=libro_id)
        except Libro.DoesNotExist:
            raise forms.ValidationError("No existe el libro con ese ID")
        return libro_id