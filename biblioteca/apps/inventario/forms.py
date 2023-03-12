from django import forms
from .models import Prestamo
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
    id_usuario = forms.CharField(label='ID Usuario')

    class Meta:
        model = Prestamo
        fields = ['id_usuario', 'ejemplar', 'fecha_prestamo']