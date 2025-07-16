# django
from datetime import timedelta
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import FormView
from django.contrib import messages
import pandas as pd

# propios
from contratos.forms import ArchivoCargaForm
from contratos.models import Contract
from clientes.models import Client
from vehiculos.models import Car
from invoices.models import Invoice

class CargaArchivoView(FormView):
    template_name = "carga_archivo.html"
    form_class = ArchivoCargaForm
    success_url = reverse_lazy("carga-archivo")

    def form_valid(self, form):

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

            for _, fila in df.iterrows():

                cliente, _ = Client.objects.get_or_create(
                    documento=str(fila["Número de documento"]),
                    defaults={
                        "nombres": fila["Nombres"],
                        "apellidos": fila["Apellidos"],
                    }
                )

                auto, _ = Car.objects.get_or_create(
                    placa=fila["Placa del auto"],
                    defaults={
                        "marca": fila["Marca del auto"],
                        "modelo": fila["Modelo del auto"],
                    }
                )

                fecha_inicio = parse_date(str(fila["Inicio de contrato"]))
                contrato = Contract.objects.create(
                    client=cliente,
                    car=auto,
                    cuota_semanal=fila["Cuota semanal"],
                    semanas=52,
                    fecha_inicio=fecha_inicio
                )

                for semana in range(52):
                    vencimiento = fecha_inicio + timedelta(weeks=semana)
                    Invoice.objects.create(
                        contract=contrato,
                        monto=fila["Cuota semanal"],
                        numero_cuota=semana + 1,
                        fecha_vencimiento=vencimiento
                    )

            messages.success(self.request, "Archivo cargado y datos registrados exitosamente.")
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Error al procesar archivo: {str(e)}")
            return self.form_invalid(form)