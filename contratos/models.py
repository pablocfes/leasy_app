from django.db import models
from django.core.validators import MinValueValidator
from vehiculos.models import Carro
from clientes.models import Cliente
from core.models import AuditoriaMixin


# Create your models here.
class Contrato(AuditoriaMixin):
    """
    Representa un contrato de alquiler entre un cliente y un auto.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='contratos', verbose_name="Cliente")
    carro = models.ForeignKey(Carro, on_delete=models.PROTECT, related_name='contratos', verbose_name="Carro")
    cuota_semanal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Cuota semanal"
    )
    semanas_totales = models.PositiveIntegerField(verbose_name="Total de semanas")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ['-fecha_inicio']
        constraints = [
            models.UniqueConstraint(
                fields=['cliente'],
                condition=models.Q(activo=True),
                name='contrato_activo_unico_por_cliente'
            ),
            models.UniqueConstraint(
                fields=['carro'],
                condition=models.Q(activo=True),
                name='contrato_activo_unico_por_carro'
            )
        ]

    def __str__(self):
        return f"Contrato #{self.id} - {self.cliente} - {self.auto}"
