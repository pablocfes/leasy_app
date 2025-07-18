
from clientes.views import ListarClientesView, EditarClienteView
from django.urls import path

app_name = 'clientes'

urlpatterns = [
    path('listar/', ListarClientesView.as_view(), name='listar'),
    path('editar/<int:pk>/', EditarClienteView.as_view(), name='editar'),
]
