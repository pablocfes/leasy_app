from django.db import models
from django.utils import timezone
from contratos.models import Contract

# Create your models here.
class Invoice(models.Model):
    """
    Representa una cuota que el cliente debe pagar.
    """
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name='invoices', verbose_name="Contrato")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    installment_number = models.PositiveIntegerField(verbose_name="Número de cuota")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    due_date = models.DateField(verbose_name="Fecha de vencimiento")
    payment_date = models.DateField(blank=True, null=True, verbose_name="Fecha de pago")
    is_paid = models.BooleanField(default=False, verbose_name="Pagada")

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['contract', 'installment_number']
        unique_together = ['contract', 'installment_number']

    def __str__(self):
        return f"Cuota #{self.installment_number} - {self.contract}"

    def save(self, *args, **kwargs):
        # Actualizar el estado de pago según la fecha de pago
        if self.payment_date and not self.is_paid:
            self.is_paid = True
        elif not self.payment_date and self.is_paid:
            self.is_paid = False
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return not self.is_paid and self.due_date < timezone.now().date()