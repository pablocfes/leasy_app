from core.views_genericos import ModeloDinamicoListView
from vehiculos.models import Carro

class ListarVehiculosView(ModeloDinamicoListView):
    model = Carro

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Vehículos'
        return context