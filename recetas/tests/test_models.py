from django.test import TestCase
from django.contrib.auth.models import User
from recetas.models import Receta, Categoria, Tag, Valoracion
from recetas.forms import RecetaForm, BusquedaForm


class RecetaModelTest(TestCase):
    """Tests para el modelo Receta."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.categoria = Categoria.objects.create(
            nombre='Postres',
            descripcion='Recetas de postres deliciosos'
        )
        
        self.tag = Tag.objects.create(
            nombre='Chocolate',
            descripcion='Recetas con chocolate'
        )
        
        self.receta = Receta.objects.create(
            titulo='Torta de Chocolate',
            descripcion='Una deliciosa torta de chocolate',
            ingredientes='Chocolate\nHuevos\nHarina\nAzúcar',
            instrucciones='Mezclar ingredientes\nHornear 45 minutos',
            tiempo_preparacion=60,
            porciones=8,
            dificultad='medio',
            categoria=self.categoria,
            creador=self.user
        )
        
        self.receta.tags.add(self.tag)
    
    def test_receta_creation(self):
        """Test de creación de receta."""
        self.assertEqual(self.receta.titulo, 'Torta de Chocolate')
        self.assertEqual(self.receta.creador, self.user)
        self.assertEqual(self.receta.categoria, self.categoria)
        self.assertTrue(self.receta.activa)
    
    def test_receta_str(self):
        """Test del método __str__ de Receta."""
        self.assertEqual(str(self.receta), 'Torta de Chocolate')
    
    def test_receta_slug_generation(self):
        """Test de generación automática de slug."""
        self.assertEqual(self.receta.slug, 'torta-de-chocolate')
    
    def test_receta_ingredients_list(self):
        """Test del método ingredientes_lista."""
        ingredientes = self.receta.ingredientes_lista()
        expected = ['Chocolate', 'Huevos', 'Harina', 'Azúcar']
        self.assertEqual(ingredientes, expected)
    
    def test_receta_instructions_list(self):
        """Test del método instrucciones_lista."""
        instrucciones = self.receta.instrucciones_lista()
        expected = ['Mezclar ingredientes', 'Hornear 45 minutos']
        self.assertEqual(instrucciones, expected)
    
    def test_receta_valoracion_promedio(self):
        """Test del método valoracion_promedio."""
        # Sin valoraciones
        self.assertEqual(self.receta.valoracion_promedio(), 0)
        
        # Con valoraciones
        Valoracion.objects.create(
            receta=self.receta,
            usuario=self.user,
            puntuacion=5,
            comentario='Excelente'
        )
        
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        Valoracion.objects.create(
            receta=self.receta,
            usuario=user2,
            puntuacion=3,
            comentario='Buena'
        )
        
        self.assertEqual(self.receta.valoracion_promedio(), 4.0)
    
    def test_receta_total_valoraciones(self):
        """Test del método total_valoraciones."""
        # Sin valoraciones
        self.assertEqual(self.receta.total_valoraciones(), 0)
        
        # Con valoraciones
        Valoracion.objects.create(
            receta=self.receta,
            usuario=self.user,
            puntuacion=5,
            comentario='Excelente'
        )
        
        self.assertEqual(self.receta.total_valoraciones(), 1)


class CategoriaModelTest(TestCase):
    """Tests para el modelo Categoria."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.categoria = Categoria.objects.create(
            nombre='Postres',
            descripcion='Recetas de postres deliciosos'
        )
    
    def test_categoria_creation(self):
        """Test de creación de categoría."""
        self.assertEqual(self.categoria.nombre, 'Postres')
        self.assertEqual(self.categoria.descripcion, 'Recetas de postres deliciosos')
        self.assertTrue(self.categoria.activa)
    
    def test_categoria_str(self):
        """Test del método __str__ de Categoria."""
        self.assertEqual(str(self.categoria), 'Postres')
    
    def test_categoria_slug_generation(self):
        """Test de generación automática de slug."""
        self.assertEqual(self.categoria.slug, 'postres')


class TagModelTest(TestCase):
    """Tests para el modelo Tag."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.tag = Tag.objects.create(
            nombre='Chocolate',
            descripcion='Recetas con chocolate'
        )
    
    def test_tag_creation(self):
        """Test de creación de tag."""
        self.assertEqual(self.tag.nombre, 'Chocolate')
        self.assertEqual(self.tag.descripcion, 'Recetas con chocolate')
    
    def test_tag_str(self):
        """Test del método __str__ de Tag."""
        self.assertEqual(str(self.tag), 'Chocolate')
    
    def test_tag_slug_generation(self):
        """Test de generación automática de slug."""
        self.assertEqual(self.tag.slug, 'chocolate')


class ValoracionModelTest(TestCase):
    """Tests para el modelo Valoracion."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.categoria = Categoria.objects.create(
            nombre='Postres',
            descripcion='Recetas de postres deliciosos'
        )
        
        self.receta = Receta.objects.create(
            titulo='Torta de Chocolate',
            descripcion='Una deliciosa torta de chocolate',
            ingredientes='Chocolate\nHuevos\nHarina\nAzúcar',
            instrucciones='Mezclar ingredientes\nHornear 45 minutos',
            tiempo_preparacion=60,
            porciones=8,
            dificultad='medio',
            categoria=self.categoria,
            creador=self.user
        )
        
        self.valoracion = Valoracion.objects.create(
            receta=self.receta,
            usuario=self.user,
            puntuacion=5,
            comentario='Excelente receta'
        )
    
    def test_valoracion_creation(self):
        """Test de creación de valoración."""
        self.assertEqual(self.valoracion.receta, self.receta)
        self.assertEqual(self.valoracion.usuario, self.user)
        self.assertEqual(self.valoracion.puntuacion, 5)
        self.assertEqual(self.valoracion.comentario, 'Excelente receta')
    
    def test_valoracion_str(self):
        """Test del método __str__ de Valoracion."""
        expected = f'{self.receta.titulo} - {self.user.username} (5/5)'
        self.assertEqual(str(self.valoracion), expected)
    
    def test_valoracion_unique_constraint(self):
        """Test de restricción única (usuario-receta)."""
        with self.assertRaises(Exception):
            Valoracion.objects.create(
                receta=self.receta,
                usuario=self.user,
                puntuacion=3,
                comentario='Otra valoración'
            )


class RecetaFormTest(TestCase):
    """Tests para el formulario RecetaForm."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.categoria = Categoria.objects.create(
            nombre='Postres',
            descripcion='Recetas de postres deliciosos'
        )
    
    def test_receta_form_valid(self):
        """Test de formulario válido."""
        form_data = {
            'titulo': 'Torta de Chocolate',
            'descripcion': 'Una deliciosa torta',
            'ingredientes': 'Chocolate\nHuevos\nHarina',
            'instrucciones': 'Mezclar\nHornear',
            'tiempo_preparacion': 60,
            'porciones': 8,
            'dificultad': 'medio',
            'categoria': self.categoria.id,
        }
        
        form = RecetaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_receta_form_invalid(self):
        """Test de formulario inválido."""
        form_data = {
            'titulo': '',  # Campo requerido vacío
            'descripcion': 'Una deliciosa torta',
            'ingredientes': 'Chocolate\nHuevos\nHarina',
            'instrucciones': 'Mezclar\nHornear',
            'tiempo_preparacion': 60,
            'porciones': 8,
            'dificultad': 'medio',
            'categoria': self.categoria.id,
        }
        
        form = RecetaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)
    
    def test_receta_form_tiempo_preparacion_validation(self):
        """Test de validación de tiempo de preparación."""
        form_data = {
            'titulo': 'Torta de Chocolate',
            'descripcion': 'Una deliciosa torta',
            'ingredientes': 'Chocolate\nHuevos\nHarina',
            'instrucciones': 'Mezclar\nHornear',
            'tiempo_preparacion': 0,  # Tiempo inválido
            'porciones': 8,
            'dificultad': 'medio',
            'categoria': self.categoria.id,
        }
        
        form = RecetaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tiempo_preparacion', form.errors)
    
    def test_receta_form_porciones_validation(self):
        """Test de validación de porciones."""
        form_data = {
            'titulo': 'Torta de Chocolate',
            'descripcion': 'Una deliciosa torta',
            'ingredientes': 'Chocolate\nHuevos\nHarina',
            'instrucciones': 'Mezclar\nHornear',
            'tiempo_preparacion': 60,
            'porciones': 0,  # Porciones inválidas
            'dificultad': 'medio',
            'categoria': self.categoria.id,
        }
        
        form = RecetaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('porciones', form.errors)


class BusquedaFormTest(TestCase):
    """Tests para el formulario BusquedaForm."""
    
    def test_busqueda_form_valid(self):
        """Test de formulario de búsqueda válido."""
        form_data = {
            'q': 'chocolate',
            'categoria': '',
            'dificultad': '',
            'tiempo_max': '',
        }
        
        form = BusquedaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_busqueda_form_empty(self):
        """Test de formulario de búsqueda vacío."""
        form_data = {}
        
        form = BusquedaForm(data=form_data)
        self.assertTrue(form.is_valid())  # Todos los campos son opcionales
