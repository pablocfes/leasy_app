# django imports
from django.views.generic import TemplateView

# local imports
from core.mixins import LoginRequiredMixin
from usuarios.models import Usuario
from clientes.models import Cliente
from vehiculos.models import Carro
from contratos.models import Contrato


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios_count'] = Usuario.objects.filter(is_active=True).count()
        context['clientes_count'] = Cliente.objects.count()
        context['vehiculos_count'] = Carro.objects.filter(disponible=True).count()
        context['contratos_count'] = Contrato.objects.filter(activo=True).count()

        contratos = Contrato.objects.select_related('cliente', 'carro').all().order_by('-fecha_inicio')

        context['titulo'] = "Contratos recientes"
        context['columnas'] = ['ID', 'Cliente', 'Numero Idetificación', 'Placa Vehículo', 'Marca', 'Modelo', 'Fecha Inicio Contrato', 'Estado']
        context['filas'] = [
            [
                contrato.id,
                str(contrato.cliente.get_full_name()),
                contrato.cliente.numero_documento,
                str(contrato.carro.placa),
                str(contrato.carro.marca),
                str(contrato.carro.modelo),
                contrato.fecha_inicio.strftime('%Y-%m-%d'),
                'Activo' if contrato.activo else 'Inactivo'
            ]
            for contrato in contratos
        ]

        return context
