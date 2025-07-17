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
    template_name = 'base_list.html'
    model = None
    fields = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todos los objetos y los campos
        queryset = self.model.objects.all()

        fields_copy = list(self.model._meta.fields)
        fields = [field.verbose_name for field in fields_copy.filter(
            name__in=['usuario_creacion_id', 'usuario_modificacion_id', 'fecha_modificacion'])]
        field_names = [field.name for field in fields_copy.exclude(
            name__in=['usuario_creacion_id', 'usuario_modificacion_id', 'fecha_modificacion'])]

        # Convertimos queryset a lista de dicts
        rows = list(queryset.values(*field_names))

        context['titulo'] = self.model._meta.verbose_name_plural.title()
        context['columnas'] = fields
        context['filas'] = rows
        return context