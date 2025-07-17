
from clientes.views import ListarClientesView
from django.urls import path

urlpatterns = [
    path('listar/', ListarClientesView.as_view(), name='listar'),
]
