from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def filter_estado(queryset, estado):
    """Filtra el queryset por estado"""
    return queryset.filter(estado=estado)

@register.filter
def add_days(date_str, days):
    """Agrega días a una fecha (para mostrar fecha de expiración)"""
    try:
        if hasattr(date_str, 'strftime'):  # Si es un objeto fecha
            new_date = date_str + timedelta(days=int(days))
            return new_date.strftime("%d/%m/%Y")
    except:
        pass
    return f"{date_str} + {days} días"