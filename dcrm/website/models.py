from django.db import models
from django.core.validators import RegexValidator

class Cliente(models.Model):
    # Validadores Regex (Backend Layer 3)
    letras_regex = RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Solo se permiten letras y espacios en este campo.')
    telefono_regex = RegexValidator(r'^\+?[\d\s\-\(\)]+$', 'El número de teléfono contiene caracteres no válidos.')
    alfa_num_regex = RegexValidator(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.,#-]+$', 'Contiene caracteres especiales no permitidos.')

    fecha_registro = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=100, validators=[letras_regex])
    apellido = models.CharField(max_length=100, validators=[letras_regex])
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, validators=[telefono_regex])
    direccion = models.CharField(max_length=255, validators=[alfa_num_regex])
    ciudad = models.CharField(max_length=100, validators=[letras_regex])
    estado = models.CharField(max_length=100, validators=[letras_regex])
    codigo_postal = models.CharField(max_length=20, validators=[RegexValidator(r'^[\d\-a-zA-Z]+$', 'Formato de código postal no válido')])

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
