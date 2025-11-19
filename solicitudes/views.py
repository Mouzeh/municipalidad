from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from .models import Solicitud
from .forms import SolicitudForm, BusquedaSolicitudForm

def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, '¡Solicitud creada exitosamente! Su solicitud está en estado PENDIENTE.')
                return redirect('crear_solicitud')
            except Exception as e:
                messages.error(request, f'Error al crear la solicitud: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = SolicitudForm()
    
    return render(request, 'solicitudes/crear.html', {'form': form})

def listar_solicitudes(request):
    # Obtener parámetro de filtro
    estado_filtro = request.GET.get('estado', '')
    
    if estado_filtro:
        solicitudes = Solicitud.objects.filter(estado=estado_filtro).order_by('-fecha_solicitud')
    else:
        solicitudes = Solicitud.objects.all().order_by('-fecha_solicitud')
    
    # Verificar expiración para cada solicitud

    for solicitud in solicitudes:
        solicitud.verificar_expiracion()
    
    context = {
        'solicitudes': solicitudes,
    }
    return render(request, 'solicitudes/listar.html', context)


#Exepciones del 404 para no romper la APP en caso de no enctrar la solicitud. 

def detalle_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    solicitud.verificar_expiracion()
    return render(request, 'solicitudes/detalle.html', {'solicitud': solicitud})

def editar_estado(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Solicitud.ESTADOS):
            solicitud.estado = nuevo_estado
            if nuevo_estado == 'ACEPTADA':
                solicitud.fecha_aceptacion = timezone.now()
            elif nuevo_estado != 'ACEPTADA':
                solicitud.fecha_aceptacion = None
            
            solicitud.save()
            messages.success(request, f'Estado actualizado a {solicitud.get_estado_display()}')
            return redirect('detalle_solicitud', id=id)
        else:
            messages.error(request, 'Estado inválido')
    
    return render(request, 'solicitudes/editar_estado.html', {'solicitud': solicitud})

def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    
    if request.method == 'POST':
        rut = solicitud.rut
        solicitud.delete()
        messages.success(request, f'Solicitud de {rut} eliminada exitosamente')
        return redirect('listar_solicitudes')
    
    return render(request, 'solicitudes/confirmar_eliminar.html', {'solicitud': solicitud})

def buscar_solicitud(request):
    resultados = None
    form = BusquedaSolicitudForm()
    rut_buscado = ""
    
    if request.method == 'POST':
        form = BusquedaSolicitudForm(request.POST)
        if form.is_valid():
            rut_buscado = form.cleaned_data['rut'].upper().strip()
            resultados = Solicitud.objects.filter(rut=rut_buscado)
            
            # Verificar expiración para cada resultado
            for solicitud in resultados:
                solicitud.verificar_expiracion()
            
            if not resultados:
                messages.info(request, f'No se encontraron solicitudes para el RUT: {rut_buscado}')
    
    context = {
        'form': form,
        'resultados': resultados,
        'rut_buscado': rut_buscado
    }
    return render(request, 'solicitudes/buscar.html', context)