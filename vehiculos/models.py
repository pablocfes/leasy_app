from django.db import models
from core.models import AuditoriaMixin
# Create your models here.
class Car(AuditoriaMixin):
    """
    Representa un auto disponible para alquiler.
    """
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="Placa")
    make = models.CharField(max_length=50, verbose_name="Marca")
    model = models.CharField(max_length=50, verbose_name="Modelo")
    year = models.IntegerField(verbose_name="Año de fabricación")
    color = models.CharField(max_length=30, blank=True, null=True, verbose_name="Color")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        verbose_name = "Auto"
        verbose_name_plural = "Autos"
        ordering = ['make', 'model']

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"
