from core.views_genericos import ModeloDinamicoListView
from invoices.models import Invoice

class ListarInvoicesView(ModeloDinamicoListView):
    model = Invoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Facturas'
        return context