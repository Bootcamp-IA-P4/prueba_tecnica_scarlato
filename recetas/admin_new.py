from django.contrib import admin
from django.utils.html import format_html
from .models import Receta, Categoria, Tag, Valoracion


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'activa', 'fecha_creacion']
    list_editable = ['activa']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ['fecha_creacion', 'total_recetas']
    
    def total_recetas(self, obj):
        """Mostrar total de recetas en la categoría"""
        return obj.recetas.count()
    total_recetas.short_description = 'Total Recetas'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'total_recetas']
    search_fields = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}
    
    def total_recetas(self, obj):
        """Mostrar total de recetas con este tag"""
        return obj.recetas.count()
    total_recetas.short_description = 'Total Recetas'


class ValoracionInline(admin.TabularInline):
    model = Valoracion
    extra = 0
    readonly_fields = ['fecha']


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'imagen_preview', 'categoria', 'dificultad', 
        'tiempo_preparacion', 'porciones', 'activa', 'fecha_creacion'
    ]
    list_filter = [
        'dificultad', 'categoria', 'activa', 'fecha_creacion'
    ]
    search_fields = ['titulo', 'ingredientes', 'descripcion']
    readonly_fields = [
        'slug', 'fecha_creacion', 'fecha_actualizacion'
    ]
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ('titulo',)}
    list_editable = ['activa']
    list_per_page = 20
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'slug', 'descripcion', 'creador')
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
        ('Contenido', {
            'fields': ('ingredientes', 'instrucciones')
        }),
        ('Clasificación', {
            'fields': ('categoria', 'dificultad', 'tags')
        }),
        ('Detalles', {
            'fields': ('tiempo_preparacion', 'porciones')
        }),
        ('Control', {
            'fields': ('activa',)
        }),
    )
    
    inlines = [ValoracionInline]
    
    def imagen_preview(self, obj):
        """Vista previa pequeña de la imagen"""
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;">',
                obj.imagen.url
            )
        return "Sin imagen"
    imagen_preview.short_description = 'Imagen'


@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ['receta', 'usuario', 'puntuacion_stars', 'comentario_corto', 'fecha']
    list_filter = ['puntuacion', 'fecha']
    search_fields = ['receta__titulo', 'usuario__username', 'comentario']
    readonly_fields = ['fecha']
    
    def puntuacion_stars(self, obj):
        """Mostrar puntuación como estrellas"""
        stars = '★' * obj.puntuacion + '☆' * (5 - obj.puntuacion)
        return format_html(
            '<span style="color: gold; font-size: 16px;">{}</span>',
            stars
        )
    puntuacion_stars.short_description = 'Puntuación'
    
    def comentario_corto(self, obj):
        """Mostrar comentario truncado"""
        return obj.comentario[:50] + '...' if len(obj.comentario) > 50 else obj.comentario
    comentario_corto.short_description = 'Comentario'


# Personalización del admin site
admin.site.site_header = "Administración de Recetas Gourmet"
admin.site.site_title = "Recetas Admin"
admin.site.index_title = "Panel de Administración"
