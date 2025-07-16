from django.db import models
# Create your models here.

class AuditoriaMixin(models.Model):
    """
    Clase para agregar campos genéricos de auditoría
    """

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion_id = models.IntegerField()

    fecha_modificacion = models.DateTimeField(null=True, auto_now=True)
    usuario_modificacion_id = models.IntegerField(null=True)

    class Meta:
        abstract = True