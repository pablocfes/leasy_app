from django.db import models
from django.core.validators import MinValueValidator
from vehiculos.models import Car
from clientes.models import Client


# Create your models here.
class Contract(models.Model):
    """
    Representa un contrato de alquiler entre un cliente y un auto.
    """
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='contracts', verbose_name="Cliente")
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='contracts', verbose_name="Auto")
    weekly_payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Cuota semanal"
    )
    total_weeks = models.PositiveIntegerField(verbose_name="Total de semanas")
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de finalización")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ['-start_date']
        constraints = [
            models.UniqueConstraint(
                fields=['client'],
                condition=models.Q(is_active=True),
                name='unique_active_client_contract'
            ),
            models.UniqueConstraint(
                fields=['car'],
                condition=models.Q(is_active=True),
                name='unique_active_car_contract'
            )
        ]

    def __str__(self):
        return f"Contrato #{self.id} - {self.client} - {self.car}"

    def save(self, *args, **kwargs):
        if self.is_active:
            Contract.objects.filter(client=self.client, is_active=True).exclude(id=self.id).update(is_active=False)
            Contract.objects.filter(car=self.car, is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)