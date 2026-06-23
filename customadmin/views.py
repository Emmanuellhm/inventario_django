from django.views.generic import TemplateView

class ContactView(TemplateView):
    template_name = 'customadmin/contact.html'
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.contrib import messages
from roles.decorators import role_required

class CustomLoginView(LoginView):
    template_name = 'customadmin/login.html'

class CustomLogoutView(LogoutView):
    next_page = '/adminpanel/login/'

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from dcrm.website.models import Cliente
from django.contrib.admin.views.decorators import staff_member_required

@role_required('admin')
def dashboard(request):
    clientes = Cliente.objects.all().order_by('-id')
    total_clientes = clientes.count()
    ciudades_unicas = clientes.values('ciudad').distinct().count()
    estados_unicos = clientes.values('estado').distinct().count()

    context = {
        'total_clientes': total_clientes,
        'ciudades_unicas': ciudades_unicas,
        'estados_unicos': estados_unicos,
    }
    return render(request, 'customadmin/dashboard.html', context)

def no_access(request):
    messages.error(request, "No tienes permiso para acceder a esta página.")
    return render(request, 'customadmin/no_access.html')

# Contact page for navbar link
def contacto(request):
    return render(request, 'customadmin/contacto.html')

@method_decorator(role_required('admin'), name='dispatch')
class ClienteListView(ListView):
    model = Cliente
    template_name = 'customadmin/cliente_list.html'
    context_object_name = 'clientes'

from dcrm.website.forms import ClienteForm

@method_decorator(role_required('admin'), name='dispatch')
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'customadmin/cliente_form.html'
    success_url = reverse_lazy('customadmin:cliente_list')

@method_decorator(role_required('admin'), name='dispatch')
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'customadmin/cliente_form.html'
    success_url = reverse_lazy('customadmin:cliente_list')

@method_decorator(role_required('admin'), name='dispatch')
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'customadmin/cliente_confirm_delete.html'
    success_url = reverse_lazy('customadmin:cliente_list')

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

@role_required('admin')
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'customadmin/cliente_detail.html', {'cliente': cliente})

@role_required('admin')
def download_pdf(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cliente_{cliente.nombre}_{cliente.apellido}.pdf"'

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
    except ImportError:
        return HttpResponse("Error: ReportLab library is not installed.", status=500)

    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []

    styles = getSampleStyleSheet()

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

    banner_data = [
        [
            Paragraph("LF CARPINTER CRM", banner_style),
            Paragraph(f"<b>FICHA DE REGISTRO (ADMIN)</b><br/>ID: #{cliente.id}<br/>Fecha: {cliente.fecha_registro.strftime('%d/%m/%Y %H:%M')}", banner_sub)
        ]
    ]
    banner_table = Table(banner_data, colWidths=[280, 240])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F59E0B')),
        ('PADDING', (0,0), (-1,-1), 18),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 20),
        ('TOPPADDING', (0,0), (-1,-1), 20),
    ]))

    story.append(banner_table)
    story.append(Spacer(1, 25))

    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=colors.HexColor('#1E1B4B'),
        spaceAfter=15
    )
    story.append(Paragraph("DETALLES TÉCNICOS Y UBICACIÓN", section_title_style))

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

    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        textColor=colors.HexColor('#64748B'),
        alignment=1,
        leading=12
    )
    story.append(Paragraph("Este documento es un extracto oficial en PDF generado automáticamente por el panel de administración LF Carpinter CRM.<br/>© 2026 LF Carpinter. Todos los derechos reservados.", footer_style))

    doc.build(story)
    return response
