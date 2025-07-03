from django import forms
from django.core.exceptions import ValidationError
from .models import Receta, Categoria, Tag


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = [
            'titulo', 'descripcion', 'imagen', 'url_imagen', 'ingredientes', 
            'pasos', 'tiempo_preparacion', 'tiempo_coccion', 'porciones',
            'dificultad', 'tipo_comida', 'categoria', 'calificacion',
            'es_favorita', 'notas', 'tags'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el título de la receta'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción breve de la receta'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'url_imagen': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://ejemplo.com/imagen.jpg'
            }),
            'ingredientes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Lista los ingredientes, uno por línea'
            }),
            'pasos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe los pasos de preparación'
            }),
            'tiempo_preparacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '30',
                'min': '1'
            }),
            'tiempo_coccion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0'
            }),
            'porciones': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '4',
                'min': '1'
            }),
            'dificultad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo_comida': forms.Select(attrs={
                'class': 'form-select'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'calificacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5'
            }),
            'es_favorita': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales (opcional)'
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar queryset para categorías activas
        self.fields['categoria'].queryset = Categoria.objects.filter(activa=True)
        
        # Hacer algunos campos opcionales en el formulario
        self.fields['url_imagen'].required = False
        self.fields['imagen'].required = False
        self.fields['categoria'].required = False
        self.fields['calificacion'].required = False
        self.fields['notas'].required = False
        self.fields['tags'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        imagen = cleaned_data.get('imagen')
        url_imagen = cleaned_data.get('url_imagen')
        
        # Validar que se proporcione al menos una imagen
        if not imagen and not url_imagen:
            raise ValidationError("Debe proporcionar una imagen o una URL de imagen")
        
        # Validar tiempo de preparación
        tiempo_prep = cleaned_data.get('tiempo_preparacion')
        if tiempo_prep and tiempo_prep < 1:
            raise ValidationError("El tiempo de preparación debe ser mayor a 0")
        
        # Validar porciones
        porciones = cleaned_data.get('porciones')
        if porciones and porciones < 1:
            raise ValidationError("El número de porciones debe ser mayor a 0")
        
        return cleaned_data
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if titulo:
            # Verificar que no exista otra receta con el mismo título (excepto la actual)
            qs = Receta.objects.filter(titulo__iexact=titulo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Ya existe una receta con este título")
        return titulo


class BusquedaForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar recetas...',
            'autocomplete': 'off'
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(activa=True),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    dificultad = forms.ChoiceField(
        choices=[('', 'Cualquier dificultad')] + Receta.DIFICULTAD_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    tipo_comida = forms.ChoiceField(
        choices=[('', 'Cualquier tipo')] + Receta.TIPO_COMIDA_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    tiempo_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tiempo máximo (min)',
            'min': '1'
        })
    )
    solo_favoritas = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'imagen', 'color_hex', 'icono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la categoría'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'color_hex': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'placeholder': '#FF6B6B'
            }),
            'icono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-utensils'
            }),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['nombre', 'color']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del tag'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'placeholder': '#FF6B6B'
            }),
        }


class RecetaRapidaForm(forms.ModelForm):
    """Formulario simplificado para agregar recetas rápidamente"""
    class Meta:
        model = Receta
        fields = ['titulo', 'descripcion', 'ingredientes', 'pasos', 'tiempo_preparacion', 'imagen', 'url_imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la receta'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción breve'
            }),
            'ingredientes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ingredientes (uno por línea)'
            }),
            'pasos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Pasos de preparación'
            }),
            'tiempo_preparacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '30',
                'min': '1'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'url_imagen': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://ejemplo.com/imagen.jpg'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen'].required = False
        self.fields['url_imagen'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        imagen = cleaned_data.get('imagen')
        url_imagen = cleaned_data.get('url_imagen')
        
        if not imagen and not url_imagen:
            raise ValidationError("Debe proporcionar una imagen o una URL de imagen")
        
        return cleaned_data
