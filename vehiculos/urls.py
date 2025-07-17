
from django.urls import path
from vehiculos.views import ListarVehiculosView

app_name = 'vehiculos'

urlpatterns = [
    path('listar/', ListarVehiculosView.as_view(), name='listar'),

]
