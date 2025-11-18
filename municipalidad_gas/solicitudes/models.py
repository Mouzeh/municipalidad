from django.db import models
from django.utils import timezone
from datetime import timedelta
import re

class Solicitud(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('ACEPTADA', 'Aceptada'),
        ('RECHAZADA', 'Rechazada'),
        ('EXPIRADA', 'Expirada'),
    ]
    
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    comuna = models.CharField(max_length=50, verbose_name="Comuna")
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    fecha_aceptacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Aceptación")
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE', verbose_name="Estado")
    
    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
    
    def __str__(self):
        return f"{self.rut} - {self.nombres} {self.apellidos}"
    
    def clean(self):
        # Validar formato RUT (simple)
        if self.rut:
            rut_pattern = re.compile(r'^\d{1,8}-[\dkK]$')
            if not rut_pattern.match(self.rut):
                raise ValidationError({'rut': 'Formato de RUT inválido. Use: 12345678-9'})
    
    def verificar_expiracion(self):
        if self.estado == 'ACEPTADA' and self.fecha_aceptacion:
            if timezone.now() > self.fecha_aceptacion + timedelta(days=30):
                self.estado = 'EXPIRADA'
                self.save()
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)