from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'direccion', 'ciudad', 'estado', 'codigo_postal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pérez'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej. juan@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. +1 (555) 123-4567'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Calle 123 #45-67'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Bogotá'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cundinamarca'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 110111'}),
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'correo': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'ciudad': 'Ciudad',
            'estado': 'Estado / Departamento',
            'codigo_postal': 'Código Postal',
        }