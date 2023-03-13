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
    cedula_usuario = forms.CharField(label='Cédula Usuario')
    id_ejemplar = forms.CharField(label='ID Ejemplar')

    class Meta:
        model = Prestamo
        fields = ['cedula_usuario', 'id_ejemplar', 'fecha_prestamo', 'fecha_devolucion' ]
        
class EjemplarForm(forms.ModelForm):
    libro_id = forms.IntegerField(label='ID del libro')
    
    class Meta:
        model = Ejemplar
        fields = ('estado', 'ubicacion', 'fecha_adquisicion', 'ultima_revision', 'cantidad', 'comentarios')
        
    def clean_libro_id(self):
        libro_id = self.cleaned_data['libro_id']
        try:
            libro = Libro.objects.get(id=libro_id)
        except Libro.DoesNotExist:
            raise forms.ValidationError("No existe el libro con ese ID")
        return libro_id