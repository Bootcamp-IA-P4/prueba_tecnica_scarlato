from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'recetas', api_views.RecetaViewSet)
router.register(r'categorias', api_views.CategoriaViewSet)
router.register(r'tags', api_views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
