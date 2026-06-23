from django import forms
# pyrefly: ignore [missing-import]
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'direccion', 'ciudad', 'estado', 'codigo_postal']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Juan',
                'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                'data-msg-required': 'El nombre es obligatorio.',
                'data-msg-pattern': 'El nombre solo puede contener letras y espacios.',
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Pérez',
                'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                'data-msg-required': 'El apellido es obligatorio.',
                'data-msg-pattern': 'El apellido solo puede contener letras y espacios.',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. juan@correo.com',
                'data-msg-required': 'El correo electrónico es obligatorio.',
                'data-msg-type': 'Ingresa un correo válido. Ejemplo: usuario@dominio.com',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. +1 (555) 123-4567',
                'pattern': r'^\+?[\d\s\-\(\)]+$',
                'data-msg-required': 'El teléfono es obligatorio.',
                'data-msg-pattern': 'Solo se permiten números, espacios, +, - y paréntesis.',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Calle 123 #45-67',
                'pattern': r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.,#-]+$',
                'data-msg-required': 'La dirección es obligatoria.',
                'data-msg-pattern': 'La dirección contiene caracteres no permitidos.',
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Bogotá',
                'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                'data-msg-required': 'La ciudad es obligatoria.',
                'data-msg-pattern': 'La ciudad solo puede contener letras y espacios.',
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Cundinamarca',
                'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                'data-msg-required': 'El estado o departamento es obligatorio.',
                'data-msg-pattern': 'El estado solo puede contener letras y espacios.',
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. 110111',
                'pattern': r'^[\d\-a-zA-Z]+$',
                'data-msg-required': 'El código postal es obligatorio.',
                'data-msg-pattern': 'El código postal solo puede contener letras, números y guiones.',
            }),
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
        error_messages = {
            'nombre': {
                'required': 'El nombre es obligatorio.',
                'max_length': 'El nombre no puede superar los %(limit_value)d caracteres.',
                'invalid': 'El nombre solo puede contener letras y espacios.',
            },
            'apellido': {
                'required': 'El apellido es obligatorio.',
                'max_length': 'El apellido no puede superar los %(limit_value)d caracteres.',
                'invalid': 'El apellido solo puede contener letras y espacios.',
            },
            'correo': {
                'required': 'El correo electrónico es obligatorio.',
                'invalid': 'Ingresa un correo válido, por ejemplo: usuario@dominio.com',
            },
            'telefono': {
                'required': 'El teléfono es obligatorio.',
                'max_length': 'El teléfono no puede superar los %(limit_value)d caracteres.',
            },
            'direccion': {
                'required': 'La dirección es obligatoria.',
                'max_length': 'La dirección no puede superar los %(limit_value)d caracteres.',
            },
            'ciudad': {
                'required': 'La ciudad es obligatoria.',
                'max_length': 'La ciudad no puede superar los %(limit_value)d caracteres.',
            },
            'estado': {
                'required': 'El estado o departamento es obligatorio.',
                'max_length': 'El estado no puede superar los %(limit_value)d caracteres.',
            },
            'codigo_postal': {
                'required': 'El código postal es obligatorio.',
                'max_length': 'El código postal no puede superar los %(limit_value)d caracteres.',
            },
        }
