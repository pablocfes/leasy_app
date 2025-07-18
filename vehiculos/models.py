from django.db import models
from core.models import AuditoriaMixin
# Create your models here.
class Carro(AuditoriaMixin):
    """
    Representa un carro.
    """
    placa = models.CharField(max_length=20, unique=True, verbose_name="Placa")
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    año_fabricacion = models.IntegerField(verbose_name="Año de fabricación", blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True, verbose_name="Color")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"
        ordering = ['marca', 'modelo']

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"
