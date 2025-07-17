# django imports
from django.shortcuts import render
from django.views.generic import TemplateView

# local imports
from core.mixins import LoginRequiredMixin
from usuarios.models import Usuario
from clientes.models import Client
from vehiculos.models import Car
from contratos.models import Contract


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios_count'] = Usuario.objects.filter(is_active=True).count()
        context['clientes_count'] = Client.objects.count()
        context['vehiculos_count'] = Car.objects.filter(is_available=True).count()
        context['contratos_count'] = Contract.objects.filter(is_active=True).count()

        return context


class ModeloDinamicoListView(TemplateView):
    """
    Vista Base para listar Modelos y sus valores de manera dinamica
    """
    template_name = 'base_list.html'
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.model.objects.all()
        campos_excluidos = ['usuario_creacion_id', 'usuario_modificacion_id', 'fecha_modificacion']

        campos_visibles = [
            field for field in self.model._meta.fields
            if field.name not in campos_excluidos
        ]

        columnas_verbose = [field.verbose_name.title() for field in campos_visibles]
        columnas_names = [field.name for field in campos_visibles]

        filas = list(queryset.values(*columnas_names))

        context['titulo'] = self.model._meta.verbose_name_plural.title()
        context['columnas'] = columnas_verbose
        context['filas'] = filas
        return context