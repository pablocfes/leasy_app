from django.shortcuts import render
from core.views_genericos import ModeloDinamicoListView, ModeloDinamicoUpdateView
from clientes.models import Cliente

# Create your views here.

class ListarClientesView(ModeloDinamicoListView):
    model = Cliente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de clientes'
        return context


class EditarClienteView(ModeloDinamicoUpdateView):
    model = Cliente
    success_url = '/clientes/listar/'
