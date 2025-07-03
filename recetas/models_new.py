from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.contrib.auth.models import User


class CategoriaManager(models.Manager):
    def with_recipe_count(self):
        return self.annotate(
            total_recetas=models.Count('recetas')
        )


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    objects = CategoriaManager()
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
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


class RecetaManager(models.Manager):
    def populares(self):
        return self.filter(activa=True).order_by('-fecha_creacion')
    
    def rapidas(self):
        return self.filter(tiempo_preparacion__lte=30, activa=True).order_by('tiempo_preparacion')


class Receta(models.Model):
    DIFICULTAD_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil'),
    ]
    
    # Campos principales
    titulo = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recetas')
    
    # Imagen
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True, verbose_name="Imagen")
    
    # Contenido
    ingredientes = models.TextField(verbose_name="Ingredientes")
    instrucciones = models.TextField(verbose_name="Instrucciones de preparación")
    
    # Metadata
    tiempo_preparacion = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], 
        verbose_name="Tiempo de preparación (minutos)"
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
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='recetas',
        verbose_name="Categoría"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='recetas')
    
    # Control
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    objects = RecetaManager()
    
    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('recetas:detalle', kwargs={'pk': self.pk})
    
    def ingredientes_lista(self):
        """Retorna lista de ingredientes"""
        return [ingrediente.strip() for ingrediente in self.ingredientes.split('\n') if ingrediente.strip()]
    
    def instrucciones_lista(self):
        """Retorna lista de instrucciones"""
        return [paso.strip() for paso in self.instrucciones.split('\n') if paso.strip()]
    
    def valoracion_promedio(self):
        """Calcula la valoración promedio"""
        valoraciones = self.valoraciones.all()
        if valoraciones.exists():
            return valoraciones.aggregate(promedio=models.Avg('puntuacion'))['promedio']
        return 0
    
    def total_valoraciones(self):
        """Total de valoraciones"""
        return self.valoraciones.count()


class Valoracion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='valoraciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Valoración'
        verbose_name_plural = 'Valoraciones'
        ordering = ['-fecha']
        unique_together = ['receta', 'usuario']
    
    def __str__(self):
        return f"{self.receta.titulo} - {self.usuario.username} ({self.puntuacion}/5)"
