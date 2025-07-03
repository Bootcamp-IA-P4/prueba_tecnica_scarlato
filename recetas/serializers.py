from rest_framework import serializers
from .models import Receta, Categoria, Tag, Valoracion


class CategoriaSerializer(serializers.ModelSerializer):
    total_recetas = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'slug', 'descripcion', 'imagen', 'color_hex', 'icono', 'total_recetas']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nombre', 'slug', 'color']


class ValoracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valoracion
        fields = ['id', 'puntuacion', 'comentario', 'fecha']


class RecetaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de recetas"""
    categoria = CategoriaSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tiempo_total = serializers.ReadOnlyField()
    imagen_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Receta
        fields = [
            'id', 'titulo', 'slug', 'descripcion_corta', 'imagen_url',
            'tiempo_preparacion', 'tiempo_total', 'porciones', 'dificultad',
            'tipo_comida', 'categoria', 'calificacion', 'es_favorita',
            'vistas', 'fecha_creacion', 'tags'
        ]


class RecetaDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalle de recetas"""
    categoria = CategoriaSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    valoraciones = ValoracionSerializer(many=True, read_only=True)
    ingredientes_lista = serializers.ReadOnlyField(source='get_ingredientes_lista')
    pasos_lista = serializers.ReadOnlyField(source='get_pasos_lista')
    tiempo_total = serializers.ReadOnlyField()
    imagen_url = serializers.ReadOnlyField()
    promedio_valoracion = serializers.SerializerMethodField()
    
    class Meta:
        model = Receta
        fields = [
            'id', 'titulo', 'slug', 'descripcion', 'descripcion_corta',
            'imagen_url', 'ingredientes', 'pasos', 'ingredientes_lista',
            'pasos_lista', 'notas', 'tiempo_preparacion', 'tiempo_coccion',
            'tiempo_total', 'porciones', 'dificultad', 'tipo_comida',
            'categoria', 'calificacion', 'es_favorita', 'vistas',
            'calorias', 'proteinas', 'carbohidratos', 'grasas',
            'fecha_creacion', 'fecha_actualizacion', 'tags',
            'valoraciones', 'promedio_valoracion'
        ]
    
    def get_promedio_valoracion(self, obj):
        valoraciones = obj.valoraciones.all()
        if valoraciones:
            return sum(v.puntuacion for v in valoraciones) / len(valoraciones)
        return 0


class RecetaCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear y actualizar recetas"""
    
    class Meta:
        model = Receta
        fields = [
            'titulo', 'descripcion', 'imagen', 'url_imagen', 'ingredientes',
            'pasos', 'notas', 'tiempo_preparacion', 'tiempo_coccion',
            'porciones', 'dificultad', 'tipo_comida', 'categoria',
            'calificacion', 'es_favorita', 'calorias', 'proteinas',
            'carbohidratos', 'grasas', 'tags'
        ]
    
    def validate(self, data):
        """Validar que se proporcione al menos una imagen"""
        imagen = data.get('imagen')
        url_imagen = data.get('url_imagen')
        
        if not imagen and not url_imagen:
            raise serializers.ValidationError(
                "Debe proporcionar una imagen o una URL de imagen"
            )
        
        return data
    
    def validate_tiempo_preparacion(self, value):
        """Validar tiempo de preparación"""
        if value < 1:
            raise serializers.ValidationError(
                "El tiempo de preparación debe ser mayor a 0"
            )
        return value
    
    def validate_porciones(self, value):
        """Validar número de porciones"""
        if value < 1:
            raise serializers.ValidationError(
                "El número de porciones debe ser mayor a 0"
            )
        return value
