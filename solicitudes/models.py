from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator

# Modelo de Usuario Extendido
class Usuario(AbstractUser):
    ROLES = (
        ('administrador', 'Administrador'),
        ('vendedor', 'Vendedor'),
    )
    
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    rol = models.CharField(max_length=20, choices=ROLES, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_rol_display() if self.rol else 'Sin rol'}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Asignar automáticamente al grupo correspondiente
        if is_new and self.rol:
            group_name = self.rol.capitalize()
            group, created = Group.objects.get_or_create(name=group_name)
            self.groups.add(group)


# Modelo de Solicitud
class Solicitud(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('entregada', 'Entregada'),
    )
    
    rut_validator = RegexValidator(
        regex=r'^\d{7,8}-[0-9Kk]$',
        message='Formato de RUT inválido. Debe ser: 12345678-9'
    )
    
    rut = models.CharField(
        max_length=12,
        validators=[rut_validator],
        verbose_name='RUT',
        help_text='Formato: 12345678-9'
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombre Completo')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.EmailField(verbose_name='Correo Electrónico')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    direccion = models.TextField(verbose_name='Dirección')
    comuna = models.CharField(max_length=100, verbose_name='Comuna')
    region = models.CharField(max_length=100, verbose_name='Región')
    
    cantidad_cilindros = models.PositiveIntegerField(
        verbose_name='Cantidad de Cilindros',
        default=1
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
        verbose_name='Estado'
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones'
    )
    
    fecha_solicitud = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Solicitud'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    usuario_asignado = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitudes_asignadas',
        verbose_name='Usuario Asignado'
    )
    
    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"Solicitud {self.rut} - {self.get_estado_display()}"