# django
from datetime import timedelta
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import FormView
from django.contrib import messages
from django.db import transaction

# third-party
import pandas as pd


# propios
from contratos.forms import ArchivoCargaForm
from contratos.models import Contrato
from clientes.models import Cliente
from vehiculos.models import Carro
from invoices.models import Invoice
from core.views_genericos import ModeloDinamicoListView
from core.mixins import LoginRequiredMixin

class ListarContratosView(ModeloDinamicoListView):
    model = Contrato

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de contratos'
        return context


class CargaArchivoContratosView(LoginRequiredMixin, FormView):
    template_name = "contratos/cargar_contratos.html"
    form_class = ArchivoCargaForm
    success_url = reverse_lazy("contratos:cargar")

    def form_valid(self, form):

        usuario_id = self.request.user.id

        COLUMNAS_REQUERIDAS = [
            "Nombres",
            "Apellidos",
            "Número de documento",
            "Inicio de contrato",
            "Cuota semanal",
            "Marca del auto",
            "Modelo del auto",
            "Placa del auto"
        ]
        archivo = form.cleaned_data["archivo"]

        try:
            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
            else:
                df = pd.read_excel(archivo)

            columnas_archivo = df.columns.tolist()
            faltantes = [col for col in COLUMNAS_REQUERIDAS if col not in columnas_archivo]

            if faltantes:
                messages.error(self.request, f"Columnas faltantes: {', '.join(faltantes)}")
                return self.form_invalid(form)

            with transaction.atomic():
                for _, fila in df.iterrows():

                    cliente, _ = Cliente.objects.get_or_create(
                        numero_documento=str(fila["Número de documento"]),
                        defaults={
                            "nombres": fila["Nombres"],
                            "apellidos": fila["Apellidos"],
                            "usuario_creacion_id": usuario_id,
                        }
                    )

                    auto, _ = Carro.objects.get_or_create(
                        placa=fila["Placa del auto"],
                        defaults={
                            "marca": fila["Marca del auto"],
                            "modelo": fila["Modelo del auto"],
                            "usuario_creacion_id": usuario_id,
                        }
                    )

                    fecha_inicio = parse_date(str(fila["Inicio de contrato"]))
                    contrato, _ = Contrato.objects.get_or_create(
                        cliente=cliente,
                        carro=auto,
                        defaults={
                            "cuota_semanal": fila["Cuota semanal"],
                            "semanas_totales": 52,
                            "fecha_inicio": fecha_inicio,
                            "usuario_creacion_id": usuario_id,
                        }

                    )

                    for semana in range(52):
                        vencimiento = fecha_inicio + timedelta(weeks=semana)
                        Invoice.objects.get_or_create(
                            contrato=contrato,
                            numero_cuota=semana + 1,
                            defaults={
                                "monto": fila["Cuota semanal"],
                                "fecha_vencimiento": vencimiento,
                                "usuario_creacion_id": usuario_id,
                            }
                        )

            messages.success(self.request, "Archivo cargado y datos registrados exitosamente.")
            return super().form_valid(form)

        except Exception as e:
            transaction.set_rollback(True)
            messages.error(self.request, f"Error al procesar archivo: {str(e)}")
            return self.form_invalid(form)

