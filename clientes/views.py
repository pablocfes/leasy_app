from django.shortcuts import render
from core.views import ModeloDinamicoListView
from clientes.models import Client

# Create your views here.

class ListarClientesView(ModeloDinamicoListView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de clientes'
        return context
