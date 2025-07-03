from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django_filters.views import FilterView
from .models import Receta, Categoria, Tag
from .forms import RecetaForm, BusquedaForm, RecetaRapidaForm
from .filters import RecetaFilter


class HomeView(TemplateView):
    template_name = 'recetas/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_recetas': Receta.objects.filter(activa=True).count(),
            'recetas_favoritas': Receta.objects.filter(es_favorita=True).count(),
            'promedio_tiempo': Receta.objects.aggregate(
                promedio=Avg('tiempo_preparacion')
            )['promedio'] or 0,
            'recetas_destacadas': Receta.objects.populares()[:6],
            'categorias': Categoria.objects.with_recipe_count().filter(activa=True)[:8],
            'recetas_recientes': Receta.objects.filter(activa=True)[:3],
        })
        return context


class RecetaListView(FilterView):
    model = Receta
    template_name = 'recetas/lista.html'
    context_object_name = 'recetas'
    paginate_by = 12
    filterset_class = RecetaFilter
    
    def get_queryset(self):
        return Receta.objects.filter(activa=True).select_related('categoria').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_recetas': self.get_queryset().count(),
            'categorias': Categoria.objects.filter(activa=True),
            'form_busqueda': BusquedaForm(self.request.GET or None),
        })
        return context


class RecetaDetailView(DetailView):
    model = Receta
    template_name = 'recetas/detalle.html'
    context_object_name = 'receta'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Receta.objects.filter(activa=True).select_related('categoria').prefetch_related('tags', 'valoraciones')
    
    def get_object(self):
        obj = super().get_object()
        obj.incrementar_vistas()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receta = self.get_object()
        context.update({
            'recetas_relacionadas': Receta.objects.filter(
                categoria=receta.categoria,
                activa=True
            ).exclude(pk=receta.pk)[:4],
            'ingredientes_lista': receta.get_ingredientes_lista(),
            'pasos_lista': receta.get_pasos_lista(),
            'promedio_valoracion': receta.valoraciones.aggregate(
                promedio=Avg('puntuacion')
            )['promedio'] or 0,
        })
        return context


class RecetaCreateView(SuccessMessageMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'recetas/crear.html'
    success_message = "¡Receta creada exitosamente! 🎉"
    
    def get_success_url(self):
        return reverse_lazy('recetas:detalle', kwargs={'slug': self.object.slug})


class RecetaUpdateView(SuccessMessageMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'recetas/editar.html'
    success_message = "¡Receta actualizada exitosamente! ✨"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_success_url(self):
        return reverse_lazy('recetas:detalle', kwargs={'slug': self.object.slug})


class RecetaDeleteView(SuccessMessageMixin, DeleteView):
    model = Receta
    template_name = 'recetas/confirmar_eliminacion.html'
    success_url = reverse_lazy('recetas:lista')
    success_message = "Receta eliminada exitosamente"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class RecetasFavoritasView(ListView):
    model = Receta
    template_name = 'recetas/favoritas.html'
    context_object_name = 'recetas'
    paginate_by = 12
    
    def get_queryset(self):
        return Receta.objects.favoritas().filter(activa=True)


class RecetasPorCategoriaView(ListView):
    model = Receta
    template_name = 'recetas/por_categoria.html'
    context_object_name = 'recetas'
    paginate_by = 12
    
    def get_queryset(self):
        categoria_slug = self.kwargs.get('categoria_slug')
        self.categoria = get_object_or_404(Categoria, slug=categoria_slug)
        return Receta.objects.filter(categoria=self.categoria, activa=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        return context


class RecetasRapidasView(ListView):
    model = Receta
    template_name = 'recetas/rapidas.html'
    context_object_name = 'recetas'
    paginate_by = 12
    
    def get_queryset(self):
        return Receta.objects.rapidas()


class RecetasPopularesView(ListView):
    model = Receta
    template_name = 'recetas/populares.html'
    context_object_name = 'recetas'
    paginate_by = 12
    
    def get_queryset(self):
        return Receta.objects.populares()


class RecetaRapidaCreateView(SuccessMessageMixin, CreateView):
    model = Receta
    form_class = RecetaRapidaForm
    template_name = 'recetas/crear_rapida.html'
    success_message = "¡Receta agregada exitosamente! 🚀"
    
    def get_success_url(self):
        return reverse_lazy('recetas:detalle', kwargs={'slug': self.object.slug})


# AJAX Views
def toggle_favorito(request, receta_id):
    """Vista AJAX para marcar/desmarcar favoritos"""
    if request.method == 'POST':
        receta = get_object_or_404(Receta, id=receta_id)
        receta.es_favorita = not receta.es_favorita
        receta.save()
        
        return JsonResponse({
            'success': True,
            'es_favorita': receta.es_favorita,
            'mensaje': 'Agregada a favoritos' if receta.es_favorita else 'Removida de favoritos'
        })
    
    return JsonResponse({'success': False})


def busqueda_ajax(request):
    """Vista AJAX para búsqueda en tiempo real"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'recetas': []})
    
    recetas = Receta.objects.filter(
        Q(titulo__icontains=query) |
        Q(ingredientes__icontains=query) |
        Q(descripcion__icontains=query),
        activa=True
    )[:10]
    
    resultados = []
    for receta in recetas:
        resultados.append({
            'id': receta.id,
            'titulo': receta.titulo,
            'descripcion_corta': receta.descripcion_corta,
            'imagen_url': receta.imagen_url,
            'url': receta.get_absolute_url(),
            'tiempo_preparacion': receta.tiempo_preparacion,
            'dificultad': receta.get_dificultad_display(),
        })
    
    return JsonResponse({'recetas': resultados})


def estadisticas_view(request):
    """Vista para mostrar estadísticas de las recetas"""
    stats = {
        'total_recetas': Receta.objects.filter(activa=True).count(),
        'favoritas': Receta.objects.filter(es_favorita=True).count(),
        'por_dificultad': {},
        'por_tipo': {},
        'promedio_tiempo': Receta.objects.aggregate(
            promedio=Avg('tiempo_preparacion')
        )['promedio'] or 0,
    }
    
    # Estadísticas por dificultad
    for dificultad_code, dificultad_name in Receta.DIFICULTAD_CHOICES:
        stats['por_dificultad'][dificultad_name] = Receta.objects.filter(
            dificultad=dificultad_code, activa=True
        ).count()
    
    # Estadísticas por tipo
    for tipo_code, tipo_name in Receta.TIPO_COMIDA_CHOICES:
        stats['por_tipo'][tipo_name] = Receta.objects.filter(
            tipo_comida=tipo_code, activa=True
        ).count()
    
    return JsonResponse(stats)
