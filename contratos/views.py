# django
from datetime import timedelta
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import FormView
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.db.utils import IntegrityError

# third-party
import pandas as pd
from io import BytesIO


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

            errores = []

            with transaction.atomic():
                for index, fila in df.iterrows():
                    try:
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
                                "disponible": False,
                                "usuario_creacion_id": usuario_id,
                            }
                        )

                        fecha_inicio_formateada = parse_date(str(fila["Inicio de contrato"]))

                        contrato, creado = Contrato.objects.get_or_create(
                            cliente=cliente,
                            carro=auto,
                            defaults={
                                "cuota_semanal": fila["Cuota semanal"],
                                "semanas_totales": 52,
                                "fecha_inicio": fecha_inicio_formateada if fecha_inicio_formateada else fila["Inicio de contrato"],
                                "usuario_creacion_id": usuario_id,
                            }
                        )

                        if not creado:
                            raise ValueError("Ya existe un contrato con este cliente y auto.")

                        for semana in range(52):
                            vencimiento = (fecha_inicio_formateada if fecha_inicio_formateada else fila["Inicio de contrato"]) + timedelta(weeks=semana)
                            Invoice.objects.get_or_create(
                                contrato=contrato,
                                numero_cuota=semana + 1,
                                defaults={
                                    "monto": fila["Cuota semanal"],
                                    "fecha_vencimiento": vencimiento,
                                    "usuario_creacion_id": usuario_id,
                                }
                            )
                    except IntegrityError as e:
                        mensaje = str(e)

                        if 'contratos_contrato.cliente_id' in mensaje:
                            error_amigable = "Ya existe un contrato activo para este cliente."
                        elif 'contratos_contrato.carro_id' in mensaje:
                            error_amigable = "Ya existe un contrato activo para este vehículo."
                        else:
                            error_amigable = "Error de integridad en la base de datos: " + mensaje

                        errores.append({
                            "Fila": index + 2,
                            "Error": error_amigable
                        })

                    except Exception as e:
                        errores.append({
                            "Fila": index + 2,
                            "Error": str(e)
                        })

                if errores:
                    raise ValueError("Errores encontrados durante la carga")

        except Exception as e:
            if 'errores' in locals() and errores:
                # Generar Excel con errores
                df_errores = pd.DataFrame(errores)
                buffer = BytesIO()
                df_errores.to_excel(buffer, index=False)
                buffer.seek(0)

                response = HttpResponse(
                    buffer,
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename=errores_carga.xlsx'
                return response
            else:
                messages.error(self.request, f"Error al procesar archivo: {str(e)}")
                return self.form_invalid(form)

        messages.success(self.request, "Archivo cargado y datos registrados exitosamente.")
        return super().form_valid(form)

