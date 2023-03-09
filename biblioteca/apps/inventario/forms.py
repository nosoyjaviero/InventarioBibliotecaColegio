from django import forms
from .models import Prestamo

class DevolucionLibroForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['devuelto']
        labels = {
            'devuelto': '¿Desea devolver el libro?',
        }
        
        
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
    class Meta:
        model = Prestamo
        fields = ['fecha_prestamo', 'fecha_devolucion', 'devuelto']