import django_filters
from django import forms
from .models import Receta, Categoria


class RecetaFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Buscar por título',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título...'
        })
    )
    
    ingredientes = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Buscar por ingredientes',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por ingredientes...'
        })
    )
    
    categoria = django_filters.ModelChoiceFilter(
        queryset=Categoria.objects.filter(activa=True),
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    dificultad = django_filters.ChoiceFilter(
        choices=Receta.DIFICULTAD_CHOICES,
        empty_label="Cualquier dificultad",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    tipo_comida = django_filters.ChoiceFilter(
        choices=Receta.TIPO_COMIDA_CHOICES,
        empty_label="Cualquier tipo",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    tiempo_preparacion = django_filters.RangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Tiempo min/max'
        })
    )
    
    porciones = django_filters.RangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Porciones min/max'
        })
    )
    
    es_favorita = django_filters.BooleanFilter(
        label='Solo favoritas',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    fecha_creacion = django_filters.DateRangeFilter(
        label='Fecha de creación',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    calificacion = django_filters.NumberFilter(
        lookup_expr='gte',
        label='Calificación mínima',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '5',
            'placeholder': 'Calificación mínima'
        })
    )
    
    class Meta:
        model = Receta
        fields = [
            'titulo', 'ingredientes', 'categoria', 'dificultad', 
            'tipo_comida', 'tiempo_preparacion', 'porciones',
            'es_favorita', 'fecha_creacion', 'calificacion'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar recetas activas
        self.queryset = self.queryset.filter(activa=True)
