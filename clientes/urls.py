
from clientes.views import ListarClientesView
from django.urls import path

app_name = 'clientes'

urlpatterns = [
    path('listar/', ListarClientesView.as_view(), name='listar'),
]
