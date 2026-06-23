from django import forms
# pyrefly: ignore [missing-import]
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'direccion', 'ciudad', 'estado', 'codigo_postal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan', 'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'title': 'Solo se permiten letras y espacios'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pérez', 'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'title': 'Solo se permiten letras y espacios'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej. juan@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. +1 (555) 123-4567', 'pattern': r'^\+?[\d\s\-\(\)]+$', 'title': 'Solo números y signos de teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Calle 123 #45-67', 'pattern': r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.,#-]+$', 'title': 'Caracteres alfanuméricos básicos permitidos'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Bogotá', 'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'title': 'Solo letras'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cundinamarca', 'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'title': 'Solo letras'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 110111', 'pattern': r'^[\d\-a-zA-Z]+$', 'title': 'Letras, números y guiones'}),
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