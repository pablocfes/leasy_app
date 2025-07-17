
from django.urls import path
from contratos.views import ListarContratosView

app_name = 'contratos'

urlpatterns = [
    path('listar/', ListarContratosView.as_view(), name='listar'),

]
