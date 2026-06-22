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
    return render(request, 'customadmin/dashboard.html')

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

@method_decorator(role_required('admin'), name='dispatch')
class ClienteCreateView(CreateView):
    model = Cliente
    fields = ['nombre', 'apellido', 'correo', 'telefono', 'direccion', 'ciudad', 'estado', 'codigo_postal']
    template_name = 'customadmin/cliente_form.html'
    success_url = reverse_lazy('customadmin:cliente_list')

@method_decorator(role_required('admin'), name='dispatch')
class ClienteUpdateView(UpdateView):
    model = Cliente
    fields = ['nombre', 'apellido', 'correo', 'telefono', 'direccion', 'ciudad', 'estado', 'codigo_postal']
    template_name = 'customadmin/cliente_form.html'
    success_url = reverse_lazy('customadmin:cliente_list')

@method_decorator(role_required('admin'), name='dispatch')
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'customadmin/cliente_confirm_delete.html'
    success_url = reverse_lazy('customadmin:cliente_list')
