from django.urls import path
from . import views

app_name = 'recetas'

urlpatterns = [
    # Vistas principales
    path('', views.HomeView.as_view(), name='index'),
    path('recetas/', views.RecetaListView.as_view(), name='lista'),
    path('recetas/<slug:slug>/', views.RecetaDetailView.as_view(), name='detalle'),
    path('crear/', views.RecetaCreateView.as_view(), name='crear'),
    path('recetas/<slug:slug>/editar/', views.RecetaUpdateView.as_view(), name='editar'),
    path('recetas/<slug:slug>/eliminar/', views.RecetaDeleteView.as_view(), name='eliminar'),
    
    # Vistas especiales
    path('favoritas/', views.RecetasFavoritasView.as_view(), name='favoritas'),
    path('categoria/<slug:categoria_slug>/', views.RecetasPorCategoriaView.as_view(), name='por_categoria'),
    path('rapidas/', views.RecetasRapidasView.as_view(), name='rapidas'),
    path('populares/', views.RecetasPopularesView.as_view(), name='populares'),
    path('crear-rapida/', views.RecetaRapidaCreateView.as_view(), name='crear_rapida'),
    
    # AJAX endpoints
    path('ajax/toggle-favorito/<int:receta_id>/', views.toggle_favorito, name='toggle_favorito'),
    path('ajax/busqueda/', views.busqueda_ajax, name='busqueda_ajax'),
    path('ajax/estadisticas/', views.estadisticas_view, name='estadisticas'),
]
