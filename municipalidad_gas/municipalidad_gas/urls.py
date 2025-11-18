from django.contrib import admin
from django.urls import path
from solicitudes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.crear_solicitud, name='crear_solicitud'),
    path('solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),
    path('solicitudes/<int:id>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('solicitudes/<int:id>/editar/', views.editar_estado, name='editar_estado'),
    path('solicitudes/<int:id>/eliminar/', views.eliminar_solicitud, name='eliminar_solicitud'),
    path('buscar/', views.buscar_solicitud, name='buscar_solicitud'),
]