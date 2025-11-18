from django import forms
from .models import Solicitud

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['rut', 'nombres', 'apellidos', 'direccion', 'telefono', 'comuna']
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9',
                'pattern': '^\\d{1,8}-[\\dkK]$',
                'title': 'Formato: 12345678-9'
            }),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9+\\s()-]{9,}',
                'title': 'Mínimo 9 caracteres numéricos'
            }),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'rut': 'RUT',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'comuna': 'Comuna',
        }

class BusquedaSolicitudForm(forms.Form):
    rut = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese RUT (12345678-9)',
            'pattern': '^\\d{1,8}-[\\dkK]$'
        }),
        label='Buscar por RUT'
    )