
from django.urls import path
from contratos.views import ListarContratosView, CargaArchivoContratosView

app_name = 'contratos'

urlpatterns = [
    path('listar/', ListarContratosView.as_view(), name='listar'),
    path('cargar/', CargaArchivoContratosView.as_view(), name='cargar'),
]
