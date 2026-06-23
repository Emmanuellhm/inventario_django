from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
import re
from roles.models import Role  # type: ignore
from roles.decorators import role_required  # type: ignore

# Usamos ReportLab para la generación de PDFs en Windows
# Esto evita errores de dependencias con GTK+ (GObject) requeridos por WeasyPrint.
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from .models import Cliente
from .forms import ClienteForm


def is_htmx(request):
    """Return True if the request is made via HTMX (header 'Hx-Request' present)."""
    return request.headers.get('Hx-Request') == 'true'


def home(request):
    """Página de inicio: redirige al dashboard si ya está autenticado, sino al login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def dashboard(request):
    """Dashboard principal: lista los clientes y muestra estadísticas con la nueva paleta."""
    clientes = Cliente.objects.all().order_by('-id')
    total_clientes = clientes.count()
    ciudades_unicas = clientes.values('ciudad').distinct().count()
    estados_unicos = clientes.values('estado').distinct().count()

    context = {
        'clientes': clientes,
        'total_clientes': total_clientes,
        'ciudades_unicas': ciudades_unicas,
        'estados_unicos': estados_unicos,
    }
    return render(request, 'dashboard.html', context)


def login_user(request):
    """Procesa el inicio de sesión del usuario."""
    if request.method != 'POST':
        return redirect('home')

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()

    if not username or not password:
        messages.error(request, 'Por favor completa ambos campos.')
        return redirect('home')

    # Sanitización Regex Básica (Capa 3 y 4 de Seguridad)
    if not re.match(r'^[\w-]{3,30}$', username):
        messages.error(request, 'Credenciales incorrectas (formato de usuario no válido).')
        return redirect('home')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('dashboard')

    messages.error(request, 'Credenciales incorrectas. Verifica tu usuario y contraseña.')
    return redirect('home')


def logout_user(request):
    """Cierra la sesión del usuario."""
    logout(request)
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('home')


def register_user(request):
    """Registra un nuevo usuario de administración."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        # Validaciones
        if not all([username, email, password1, password2]):
            messages.error(request, 'Por favor completa todos los campos obligatorios.')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')

        if len(password1) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return redirect('register')

        # Sanitización con Expresiones Regulares (Regex)
        if not re.match(r'^[\w-]{3,30}$', username):
            messages.error(request, 'El nombre de usuario solo puede tener letras, números, _ y -.')
            return redirect('register')
            
        if not re.match(r'^[A-Za-z0-9@#$%^+=]{6,}$', password1):
            messages.error(request, 'La contraseña contiene caracteres especiales no permitidos.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return redirect('register')

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        # Asignar rol base automáticamente (Seguridad de Roles)
        role, created = Role.objects.get_or_create(name='Usuario')
        user.roles.add(role)

        messages.success(request, '¡Registro exitoso! Ahora inicia sesión con tus credenciales.')
        return redirect('home')

    return render(request, 'register.html')


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def add_record(request):
    """Añade un nuevo cliente en base de datos."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente agregado exitosamente!')
            if is_htmx(request):
                # HTMX request: redirect via header
                response = HttpResponse()
                response['HX-Redirect'] = reverse('dashboard')
                return response
            return redirect('dashboard')
        else:
            messages.error(request, 'Hubo un error al guardar el cliente. Revisa el formulario.')
    else:
        form = ClienteForm()
    # GET request
    if is_htmx(request):
        return render(request, 'add_record_partial.html', {'form': form})
    return render(request, 'add_record.html', {'form': form})


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def edit_record(request, pk):
    """Actualiza la información de un cliente existente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente actualizado exitosamente!')
            if is_htmx(request):
                response = HttpResponse()
                response['HX-Redirect'] = reverse('dashboard')
                return response
            return redirect('dashboard')
        else:
            messages.error(request, 'Hubo un error al actualizar los datos. Revisa el formulario.')
    else:
        form = ClienteForm(instance=cliente)
    if is_htmx(request):
        return render(request, 'edit_record_partial.html', {'form': form, 'cliente': cliente})
    return render(request, 'edit_record.html', {'form': form, 'cliente': cliente})


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def delete_record(request, pk):
    """Elimina un cliente de la base de datos."""
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    messages.success(request, '¡El registro del cliente ha sido eliminado!')
    if is_htmx(request):
        response = HttpResponse()
        response['HX-Redirect'] = reverse('dashboard')
        return response
    return redirect('dashboard')


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def view_record(request, pk):
    """Ver la ficha completa de un cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    if is_htmx(request):
        return render(request, 'view_record_partial.html', {'cliente': cliente})
    return render(request, 'view_record.html', {'cliente': cliente})








def login_user(request):
    """Procesa el inicio de sesión del usuario."""
    if request.method != 'POST':
        return redirect('home')

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()

    if not username or not password:
        messages.error(request, 'Por favor completa ambos campos.')
        return redirect('home')

    # Sanitización Regex Básica (Capa 3 y 4 de Seguridad)
    if not re.match(r'^[\w-]{3,30}$', username):
        messages.error(request, 'Credenciales incorrectas (formato de usuario no válido).')
        return redirect('home')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('dashboard')

    messages.error(request, 'Credenciales incorrectas. Verifica tu usuario y contraseña.')
    return redirect('home')


def logout_user(request):
    """Cierra la sesión del usuario."""
    logout(request)
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('home')


def register_user(request):
    """Registra un nuevo usuario de administración."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        # Validaciones
        if not all([username, email, password1, password2]):
            messages.error(request, 'Por favor completa todos los campos obligatorios.')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')

        if len(password1) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return redirect('register')

        # Sanitización con Expresiones Regulares (Regex)
        if not re.match(r'^[\w-]{3,30}$', username):
            messages.error(request, 'El nombre de usuario solo puede tener letras, números, _ y -.')
            return redirect('register')
            
        if not re.match(r'^[A-Za-z0-9@#$%^&+=]{6,}$', password1):
            messages.error(request, 'La contraseña contiene caracteres especiales no permitidos.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return redirect('register')

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        # Asignar rol base automáticamente (Seguridad de Roles)
        role, created = Role.objects.get_or_create(name='Usuario')
        user.roles.add(role)

        messages.success(request, '¡Registro exitoso! Ahora inicia sesión con tus credenciales.')
        return redirect('home')

    return render(request, 'register.html')


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def add_record(request):
    """Añade un nuevo cliente en base de datos."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente agregado exitosamente!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Hubo un error al guardar el cliente. Revisa el formulario.')
    else:
        form = ClienteForm()
    return render(request, 'add_record.html', {'form': form})


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def edit_record(request, pk):
    """Actualiza la información de un cliente existente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente actualizado exitosamente!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Hubo un error al actualizar los datos. Revisa el formulario.')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'edit_record.html', {'form': form, 'cliente': cliente})


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def delete_record(request, pk):
    """Elimina un cliente de la base de datos."""
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    messages.success(request, '¡El registro del cliente ha sido eliminado!')
    return redirect('dashboard')


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def view_record(request, pk):
    """Ver la ficha completa de un cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'view_record.html', {'cliente': cliente})


@login_required(login_url='home')
@role_required('Usuario', 'admin')
def descargar_pdf(request, pk):
    """Genera un archivo PDF con estilos premium de Bootstrap a partir de la ficha de cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cliente_{cliente.nombre}_{cliente.apellido}.pdf"'
    
    # Creamos el documento PDF con ReportLab (independiente de GTK/WeasyPrint)
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Estilos tipográficos
    banner_style = ParagraphStyle(
        'BannerTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#FFFFFF'),
        spaceAfter=6
    )
    
    banner_sub = ParagraphStyle(
        'BannerSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#E2E8F0'),
        leading=13
    )
    
    # Banner superior
    banner_data = [
        [
            Paragraph("LF CARPINTER CRM", banner_style),
            Paragraph(f"<b>FICHA DE REGISTRO</b><br/>ID: #{cliente.id}<br/>Fecha: {cliente.fecha_registro.strftime('%d/%m/%Y %H:%M')}", banner_sub)
        ]
    ]
    banner_table = Table(banner_data, colWidths=[280, 240])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E1B4B')), # Fondo índigo oscuro
        ('PADDING', (0,0), (-1,-1), 18),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 20),
        ('TOPPADDING', (0,0), (-1,-1), 20),
    ]))
    
    story.append(banner_table)
    story.append(Spacer(1, 25))
    
    # Título de la sección
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=colors.HexColor('#1E1B4B'),
        spaceAfter=15
    )
    story.append(Paragraph("DETALLES TÉCNICOS Y UBICACIÓN", section_title_style))
    
    # Estilos de texto de la tabla
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#475569')
    )
    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#0F172A')
    )
    
    # Datos estructurados del cliente (Ficha)
    details_data = [
        [Paragraph("Nombre", label_style), Paragraph(cliente.nombre, value_style)],
        [Paragraph("Apellido", label_style), Paragraph(cliente.apellido, value_style)],
        [Paragraph("Correo Electrónico", label_style), Paragraph(cliente.correo, value_style)],
        [Paragraph("Teléfono Móvil", label_style), Paragraph(cliente.telefono, value_style)],
        [Paragraph("Dirección de Residencia", label_style), Paragraph(cliente.direccion, value_style)],
        [Paragraph("Ciudad", label_style), Paragraph(cliente.ciudad, value_style)],
        [Paragraph("Estado / Región", label_style), Paragraph(cliente.estado, value_style)],
        [Paragraph("Código Postal", label_style), Paragraph(cliente.codigo_postal, value_style)],
    ]
    
    details_table = Table(details_data, colWidths=[170, 350])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 11),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    story.append(details_table)
    story.append(Spacer(1, 40))
    
    # Pie de página
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        textColor=colors.HexColor('#64748B'),
        alignment=1, # Centrado
        leading=12
    )
    story.append(Paragraph("Este documento es un extracto oficial en PDF generado automáticamente por el sistema LF Carpinter CRM.<br/>© 2026 LF Carpinter. Todos los derechos reservados.", footer_style))
    
    doc.build(story)
    return response