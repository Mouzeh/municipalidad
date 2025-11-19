from django.contrib import admin
from .models import Solicitud

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellidos', 'comuna', 'estado', 'fecha_solicitud')
    list_filter = ('estado', 'comuna', 'fecha_solicitud')
    search_fields = ('rut', 'nombres', 'apellidos')
    readonly_fields = ('fecha_solicitud',)
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('rut', 'nombres', 'apellidos', 'telefono')
        }),
        ('Información de Dirección', {
            'fields': ('direccion', 'comuna')
        }),
        ('Estado de la Solicitud', {
            'fields': ('estado', 'fecha_solicitud', 'fecha_aceptacion')
        }),
    )