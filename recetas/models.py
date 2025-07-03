from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from PIL import Image
import os


class CategoriaManager(models.Manager):
    def with_recipe_count(self):
        return self.annotate(
            total_recetas=models.Count('recetas')
        )


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    color_hex = models.CharField(max_length=7, default='#FF6B6B')
    icono = models.CharField(max_length=50, default='fas fa-utensils')
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)
    
    objects = CategoriaManager()
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class RecetaManager(models.Manager):
    def populares(self):
        return self.filter(calificacion__gte=4, activa=True).order_by('-calificacion', '-fecha_creacion')
    
    def rapidas(self):
        return self.filter(tiempo_preparacion__lte=30, activa=True).order_by('tiempo_preparacion')
    
    def favoritas(self):
        return self.filter(es_favorita=True, activa=True).order_by('-fecha_actualizacion')
    
    def por_dificultad(self, dificultad):
        return self.filter(dificultad=dificultad, activa=True)


class Receta(models.Model):
    DIFICULTAD_CHOICES = [
        ('facil', 'Fácil'),
        ('intermedio', 'Intermedio'),
        ('dificil', 'Difícil'),
    ]
    
    TIPO_COMIDA_CHOICES = [
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('cena', 'Cena'),
        ('postre', 'Postre'),
        ('aperitivo', 'Aperitivo'),
        ('snack', 'Snack'),
        ('bebida', 'Bebida'),
    ]
    
    # Campos principales
    titulo = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descripcion = models.TextField(verbose_name="Descripción")
    descripcion_corta = models.CharField(max_length=160, blank=True, verbose_name="Descripción corta")
    
    # Imágenes
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True, verbose_name="Imagen")
    url_imagen = models.URLField(blank=True, null=True, verbose_name="URL de Imagen")
    imagen_thumbnail = models.ImageField(upload_to='recetas/thumbnails/', blank=True, null=True)
    
    # Contenido
    ingredientes = models.TextField(verbose_name="Ingredientes")
    pasos = models.TextField(verbose_name="Pasos de preparación")
    notas = models.TextField(blank=True, verbose_name="Notas adicionales")
    
    # Metadata
    tiempo_preparacion = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], 
        verbose_name="Tiempo de preparación (minutos)"
    )
    tiempo_coccion = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], 
        default=0,
        verbose_name="Tiempo de cocción (minutos)"
    )
    porciones = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], 
        default=1,
        verbose_name="Número de porciones"
    )
    
    # Clasificación
    dificultad = models.CharField(
        max_length=10, 
        choices=DIFICULTAD_CHOICES,
        default='facil',
        verbose_name="Dificultad"
    )
    tipo_comida = models.CharField(
        max_length=10, 
        choices=TIPO_COMIDA_CHOICES,
        default='almuerzo',
        verbose_name="Tipo de comida"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='recetas'
    )
    
    # Interacción
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, 
        blank=True,
        verbose_name="Calificación"
    )
    es_favorita = models.BooleanField(default=False, verbose_name="Favorita")
    vistas = models.PositiveIntegerField(default=0)
    
    # Información nutricional (opcional)
    calorias = models.PositiveIntegerField(null=True, blank=True)
    proteinas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    carbohidratos = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grasas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Campos de seguimiento
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)
    
    # Tags
    tags = models.ManyToManyField('Tag', blank=True)
    
    objects = RecetaManager()
    
    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['dificultad']),
            models.Index(fields=['tipo_comida']),
            models.Index(fields=['es_favorita']),
        ]
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('recetas:detalle', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Generar slug automáticamente
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # Generar descripción corta automáticamente
        if not self.descripcion_corta:
            self.descripcion_corta = self.descripcion[:160] + '...' if len(self.descripcion) > 160 else self.descripcion
        
        super().save(*args, **kwargs)
        
        # Crear thumbnail si hay imagen
        if self.imagen:
            self.create_thumbnail()
    
    def create_thumbnail(self):
        """Crear thumbnail de la imagen"""
        if not self.imagen:
            return
        
        try:
            img = Image.open(self.imagen.path)
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            # Guardar thumbnail
            thumb_path = self.imagen.path.replace('recetas/', 'recetas/thumbnails/')
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            img.save(thumb_path)
        except Exception as e:
            print(f"Error creando thumbnail: {e}")
    
    @property
    def tiempo_total(self):
        return self.tiempo_preparacion + self.tiempo_coccion
    
    @property
    def imagen_url(self):
        if self.imagen:
            return self.imagen.url
        elif self.url_imagen:
            return self.url_imagen
        return '/static/img/placeholder-recipe.jpg'
    
    def incrementar_vistas(self):
        self.vistas += 1
        self.save(update_fields=['vistas'])
    
    def get_ingredientes_lista(self):
        return [ingrediente.strip() for ingrediente in self.ingredientes.split('\n') if ingrediente.strip()]
    
    def get_pasos_lista(self):
        return [paso.strip() for paso in self.pasos.split('\n') if paso.strip()]


class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#FF6B6B')
    
    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Valoracion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='valoraciones')
    puntuacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Valoración'
        verbose_name_plural = 'Valoraciones'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.puntuacion} estrellas - {self.receta.titulo}"
