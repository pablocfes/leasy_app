from django.db import models
from core.models import AuditoriaMixin

# Create your models here.
class Cliente(AuditoriaMixin):
    """
    Representa a los clientes de Leasy.
    """
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    tipo_documento = models.CharField(max_length=20, verbose_name="Tipo de documento")
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name="Número de documento")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    correo = models.EmailField(blank=True, null=True, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.numero_documento})"