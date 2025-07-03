from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from .models import Receta, Categoria, Tag
from .serializers import (
    RecetaListSerializer, RecetaDetailSerializer, RecetaCreateUpdateSerializer,
    CategoriaSerializer, TagSerializer
)
from .filters import RecetaFilter


class RecetaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar recetas via API"""
    queryset = Receta.objects.filter(activa=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RecetaFilter
    search_fields = ['titulo', 'ingredientes', 'descripcion']
    ordering_fields = ['fecha_creacion', 'titulo', 'tiempo_preparacion', 'calificacion']
    ordering = ['-fecha_creacion']
    
    def get_serializer_class(self):
        """Usar diferentes serializers según la acción"""
        if self.action == 'list':
            return RecetaListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return RecetaCreateUpdateSerializer
        return RecetaDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Incrementar vistas al obtener una receta"""
        instance = self.get_object()
        instance.incrementar_vistas()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def populares(self, request):
        """Endpoint para recetas populares"""
        recetas = Receta.objects.populares()[:10]
        serializer = RecetaListSerializer(recetas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def favoritas(self, request):
        """Endpoint para recetas favoritas"""
        recetas = Receta.objects.favoritas()
        serializer = RecetaListSerializer(recetas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def rapidas(self, request):
        """Endpoint para recetas rápidas"""
        recetas = Receta.objects.rapidas()[:10]
        serializer = RecetaListSerializer(recetas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_favorito(self, request, pk=None):
        """Marcar/desmarcar como favorita"""
        receta = self.get_object()
        receta.es_favorita = not receta.es_favorita
        receta.save()
        
        return Response({
            'es_favorita': receta.es_favorita,
            'mensaje': 'Agregada a favoritos' if receta.es_favorita else 'Removida de favoritos'
        })
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Endpoint personalizado para búsqueda avanzada"""
        query = request.query_params.get('q', '')
        if query:
            recetas = self.queryset.filter(
                Q(titulo__icontains=query) | 
                Q(ingredientes__icontains=query) |
                Q(descripcion__icontains=query)
            )
        else:
            recetas = self.queryset
        
        # Aplicar paginación
        page = self.paginate_queryset(recetas)
        if page is not None:
            serializer = RecetaListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = RecetaListSerializer(recetas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Endpoint para estadísticas generales"""
        stats = {
            'total_recetas': self.queryset.count(),
            'favoritas': self.queryset.filter(es_favorita=True).count(),
            'promedio_tiempo': self.queryset.aggregate(
                promedio=Avg('tiempo_preparacion')
            )['promedio'] or 0,
            'por_dificultad': {},
            'por_tipo': {}
        }
        
        # Estadísticas por dificultad
        for dificultad_code, dificultad_name in Receta.DIFICULTAD_CHOICES:
            stats['por_dificultad'][dificultad_name] = self.queryset.filter(
                dificultad=dificultad_code
            ).count()
        
        # Estadísticas por tipo
        for tipo_code, tipo_name in Receta.TIPO_COMIDA_CHOICES:
            stats['por_tipo'][tipo_name] = self.queryset.filter(
                tipo_comida=tipo_code
            ).count()
        
        return Response(stats)


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para categorías"""
    queryset = Categoria.objects.filter(activa=True)
    serializer_class = CategoriaSerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def recetas(self, request, slug=None):
        """Obtener recetas de una categoría específica"""
        categoria = self.get_object()
        recetas = Receta.objects.filter(categoria=categoria, activa=True)
        
        # Aplicar paginación
        page = self.paginate_queryset(recetas)
        if page is not None:
            serializer = RecetaListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = RecetaListSerializer(recetas, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para tags"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
