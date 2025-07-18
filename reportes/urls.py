
from django.urls import path
from reportes import views

app_name = 'reportes'

urlpatterns = [
    path('generar-reporte/', views.GenerarReporteView.as_view(), name='generar_reporte'),
]
