from django.urls import path
from . import views

app_name = 'customadmin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/add/', views.ClienteCreateView.as_view(), name='cliente_add'),
    path('clientes/<int:pk>/edit/', views.ClienteUpdateView.as_view(), name='cliente_edit'),
    path('clientes/<int:pk>/delete/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
