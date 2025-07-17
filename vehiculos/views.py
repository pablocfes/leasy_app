from core.views import ModeloDinamicoListView
from vehiculos.models import Car

class ListarVehiculosView(ModeloDinamicoListView):
    model = Car

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Vehículos'
        return context