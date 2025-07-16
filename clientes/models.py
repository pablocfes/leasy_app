from django.db import models
from core.models import AuditoriaMixin

# Create your models here.
class Client(AuditoriaMixin):
    """
    Representa a los clientes de Leasy.
    """
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    document_type = models.CharField(max_length=20, verbose_name="Tipo de documento")
    document_number = models.CharField(max_length=50, unique=True, verbose_name="Número de documento")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    email = models.EmailField(blank=True, null=True, verbose_name="Correo electrónico")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.document_number})"