# LF Carpinter CRM

Sistema de Gestión de Clientes (CRM) desarrollado con Django, HTMX y SQLite.

![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![HTMX](https://img.shields.io/badge/Frontend-HTMX-purple)

---

## Descripción General

**LF Carpinter CRM** es una aplicación web para la gestión de clientes desarrollada para la empresa LF Carpinter.

Permite administrar fichas de clientes mediante operaciones CRUD (Crear, Consultar, Editar y Eliminar), controlando el acceso mediante autenticación y roles de usuario.

El sistema utiliza:

* Django como framework backend
* SQLite como base de datos
* HTMX para navegación SPA (Single Page Application)
* Bootstrap y Tailwind CSS para la interfaz gráfica
* ReportLab para exportación de PDFs
* Sistema de roles personalizado para control de permisos

---

# Características Principales

## Gestión de Clientes (CRUD)

Los administradores pueden:

* Crear clientes
* Consultar clientes
* Editar clientes
* Eliminar clientes
* Exportar fichas a PDF

Información almacenada por cliente:

* Nombre
* Apellido
* Correo electrónico
* Teléfono
* Dirección
* Ciudad
* Estado
* Código Postal
* Fecha de registro

---

## Sistema de Roles

### Administrador

Permisos:

* Acceso al panel administrativo
* Crear clientes
* Editar clientes
* Eliminar clientes
* Ver clientes
* Exportar PDFs

### Usuario

Permisos:

* Ver clientes
* Consultar fichas
* Acceso al dashboard

No puede:

* Crear registros
* Editar registros
* Eliminar registros

---

# Arquitectura del Proyecto

```text
inventario_django/
│
├── inventario/
│   └── settings.py
│
├── dcrm/
│   └── website/
│       ├── urls.py
│       ├── views.py
│       ├── models.py
│       ├── forms.py
│       └── templates/
│
├── customadmin/
│   ├── urls.py
│   └── views.py
│
└── roles/
```

---

# Arquitectura de Navegación

```text
Usuario
   │
   ▼
home.html (Login)
   │
   ▼
authenticate()
   │
   ├── Admin
   │      ▼
   │   Panel Administrativo
   │
   └── Usuario
          ▼
      Dashboard
```

---

# URLs Principales

| URL                  | Función             |
| -------------------- | ------------------- |
| /                    | Login               |
| /dashboard/          | Dashboard principal |
| /add_record/         | Crear cliente       |
| /edit_record/<id>/   | Editar cliente      |
| /delete_record/<id>/ | Eliminar cliente    |
| /view_record/<id>/   | Ver cliente         |
| /download_pdf/<id>/  | Exportar PDF        |

---

# Modelo de Datos

Modelo principal:

```python
class Cliente(models.Model):
    nombre
    apellido
    correo
    telefono
    direccion
    ciudad
    estado
    codigo_postal
```

Django transforma automáticamente este modelo en una tabla SQL dentro de SQLite.

Base de datos:

```text
db.sqlite3
```

---

# Formularios

El sistema utiliza ModelForms de Django.

Archivo:

```text
website/forms.py
```

Formulario principal:

```python
ClienteForm
```

Validaciones realizadas mediante:

```python
form.is_valid()
```

---

# Navegación SPA con HTMX

El sistema utiliza HTMX para evitar recargas completas de página.

Ejemplo:

```html
<a hx-get="/view_record/5/"
   hx-target="#spa-container"
   hx-push-url="true">
   Ver Cliente
</a>
```

Beneficios:

* Navegación más rápida
* Menor consumo de recursos
* Experiencia similar a una SPA moderna
* Sin necesidad de React o Vue

---

# Sistema de Autenticación

Django Authentication:

```python
authenticate()
login()
logout()
```

Proceso:

1. Validación de usuario
2. Verificación de contraseña
3. Consulta de roles
4. Redirección según permisos

---

# Modelo de Seguridad (4 Capas)

El proyecto implementa una estrategia de defensa en profundidad.

## Capa 1 – HTML5

Validación en navegador:

```html
pattern=""
required
```

Bloquea datos incorrectos antes de enviarlos.

---

## Capa 2 – Django Forms

Validación mediante:

```python
form.is_valid()
```

Evita formularios manipulados.

---

## Capa 3 – Modelo Django

Validación con:

```python
RegexValidator
```

Protege la integridad de la base de datos.

---

## Capa 4 – Validación Python

Validaciones mediante:

```python
re.match()
```

Aplicadas especialmente en:

* Login
* Registro

---

# Medidas de Seguridad Adicionales

* CSRF Protection
* Session Authentication
* Role-Based Access Control (RBAC)
* Login Required Decorators
* Password Hashing (PBKDF2)
* Django Middleware
* Validación de entrada mediante Regex
* Protección contra acceso directo a URLs restringidas

---

# Recursos Locales

Todas las dependencias frontend son servidas localmente.

No se utilizan CDNs externas.

## Librerías

* Bootstrap 5
* Tailwind CSS
* HTMX
* FontAwesome

Ubicación:

```text
website/templates/static/
```

---

# Generación de PDF

Tecnología:

```text
ReportLab
```

Permite exportar la ficha completa de un cliente a formato PDF.

Incluye:

* Datos del cliente
* Información de contacto
* Fecha de registro
* Branding de LF Carpinter

---

# Tecnologías Utilizadas

| Tecnología   | Uso                     |
| ------------ | ----------------------- |
| Python 3     | Lenguaje principal      |
| Django 5     | Framework Backend       |
| SQLite       | Base de datos           |
| HTMX         | Navegación SPA          |
| Bootstrap 5  | Diseño UI               |
| Tailwind CSS | Estilos complementarios |
| FontAwesome  | Iconografía             |
| ReportLab    | Exportación PDF         |
| django-roles | Gestión de roles        |

---

# Instalación

## Clonar repositorio

```bash
git clone https://github.com/usuario/lf-carpinter-crm.git
cd lf-carpinter-crm
```

## Crear entorno virtual

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar migraciones

```bash
python manage.py migrate
```

## Crear superusuario

```bash
python manage.py createsuperuser
```

## Iniciar servidor

```bash
python manage.py runserver
```

---

# Autor

**LF Carpinter CRM**

Sistema de Gestión de Clientes desarrollado con Django, HTMX y SQLite como proyecto académico y empresarial enfocado en seguridad, arquitectura multicapa y gestión eficiente de clientes.
