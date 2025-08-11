import django_filters
from .models import Evento

class EventoFilter(django_filters.FilterSet):
    data = django_filters.DateFilter(field_name='data', lookup_expr='exact', label='Data do evento')
    data_inicio = django_filters.DateFilter(field_name='data', lookup_expr='gte', label='A partir de')
    data_fim = django_filters.DateFilter(field_name='data', lookup_expr='lte', label='Até')

    class Meta:
        model = Evento
        fields = ['data', 'data_inicio', 'data_fim']