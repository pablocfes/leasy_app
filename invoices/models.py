from django.db import models
from django.utils import timezone
from contratos.models import Contrato
from core.models import AuditoriaMixin
# Create your models here.

class Invoice(AuditoriaMixin):
    """
    Representa una cuota que el cliente debe pagar.
    """
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='facturas', verbose_name="Contrato")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    numero_cuota = models.PositiveIntegerField(verbose_name="Número de cuota")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    fecha_pago = models.DateField(blank=True, null=True, verbose_name="Fecha de pago")
    pagada = models.BooleanField(default=False, verbose_name="Pagada")

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['contrato', 'numero_cuota']
        unique_together = ['contrato', 'numero_cuota']

    def __str__(self):
        return f"Cuota #{self.numero_cuota} - {self.contrato}"

    def save(self, *args, **kwargs):
        # Actualizar el estado de pago según la fecha de pago
        if self.fecha_pago and not self.pagada:
            self.pagada = True
        elif not self.fecha_pago and self.pagada:
            self.pagada = False
        super().save(*args, **kwargs)

    @property
    def vencida(self):
        return not self.pagada and self.fecha_vencimiento < timezone.now().date()