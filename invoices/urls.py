
from django.urls import path
from invoices.views import ListarInvoicesView

app_name = 'invoices'

urlpatterns = [
    path('listar/', ListarInvoicesView.as_view(), name='listar'),

]
