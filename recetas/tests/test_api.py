from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from recetas.models import Receta, Categoria, Tag


class RecetaAPITest(TestCase):
    """Tests para la API de recetas."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.client = APIClient()
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
    
    def test_get_recetas_list(self):
        """Test GET lista de recetas."""
        url = reverse('recetas:api:receta-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['titulo'], 'Torta de Chocolate')
    
    def test_get_receta_detail(self):
        """Test GET detalle de receta."""
        url = reverse('recetas:api:receta-detail', kwargs={'pk': self.receta.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['titulo'], 'Torta de Chocolate')
        self.assertEqual(data['descripcion'], 'Una deliciosa torta de chocolate')
        self.assertEqual(data['tiempo_preparacion'], 60)
        self.assertEqual(data['porciones'], 8)
        self.assertEqual(data['dificultad'], 'medio')
    
    def test_create_receta_authenticated(self):
        """Test POST crear receta autenticado."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'titulo': 'Nueva Receta API',
            'descripcion': 'Descripción de la nueva receta',
            'ingredientes': 'Ingrediente 1\nIngrediente 2',
            'instrucciones': 'Paso 1\nPaso 2',
            'tiempo_preparacion': 30,
            'porciones': 4,
            'dificultad': 'facil',
            'categoria': self.categoria.id,
        }
        
        url = reverse('recetas:api:receta-list')
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Receta.objects.count(), 2)
        
        nueva_receta = Receta.objects.get(titulo='Nueva Receta API')
        self.assertEqual(nueva_receta.creador, self.user)
    
    def test_create_receta_unauthenticated(self):
        """Test POST crear receta sin autenticación."""
        data = {
            'titulo': 'Nueva Receta API',
            'descripcion': 'Descripción de la nueva receta',
            'ingredientes': 'Ingrediente 1\nIngrediente 2',
            'instrucciones': 'Paso 1\nPaso 2',
            'tiempo_preparacion': 30,
            'porciones': 4,
            'dificultad': 'facil',
            'categoria': self.categoria.id,
        }
        
        url = reverse('recetas:api:receta-list')
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_receta_owner(self):
        """Test PUT actualizar receta del propietario."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'titulo': 'Torta de Chocolate Modificada',
            'descripcion': 'Descripción modificada',
            'ingredientes': 'Chocolate\nHuevos\nHarina\nAzúcar\nVainilla',
            'instrucciones': 'Mezclar ingredientes\nHornear 45 minutos\nDejar enfriar',
            'tiempo_preparacion': 75,
            'porciones': 10,
            'dificultad': 'dificil',
            'categoria': self.categoria.id,
        }
        
        url = reverse('recetas:api:receta-detail', kwargs={'pk': self.receta.id})
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        receta_modificada = Receta.objects.get(id=self.receta.id)
        self.assertEqual(receta_modificada.titulo, 'Torta de Chocolate Modificada')
        self.assertEqual(receta_modificada.tiempo_preparacion, 75)
    
    def test_update_receta_not_owner(self):
        """Test PUT actualizar receta de otro usuario."""
        otro_user = User.objects.create_user(
            username='otrouser',
            email='otro@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=otro_user)
        
        data = {
            'titulo': 'Torta de Chocolate Modificada',
            'descripcion': 'Descripción modificada',
            'ingredientes': 'Chocolate\nHuevos\nHarina\nAzúcar\nVainilla',
            'instrucciones': 'Mezclar ingredientes\nHornear 45 minutos\nDejar enfriar',
            'tiempo_preparacion': 75,
            'porciones': 10,
            'dificultad': 'dificil',
            'categoria': self.categoria.id,
        }
        
        url = reverse('recetas:api:receta-detail', kwargs={'pk': self.receta.id})
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_receta_owner(self):
        """Test DELETE eliminar receta del propietario."""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('recetas:api:receta-detail', kwargs={'pk': self.receta.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Receta.objects.count(), 0)
    
    def test_delete_receta_not_owner(self):
        """Test DELETE eliminar receta de otro usuario."""
        otro_user = User.objects.create_user(
            username='otrouser',
            email='otro@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=otro_user)
        
        url = reverse('recetas:api:receta-detail', kwargs={'pk': self.receta.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_receta_search_filter(self):
        """Test filtro de búsqueda en API."""
        # Crear otra receta
        Receta.objects.create(
            titulo='Ensalada César',
            descripcion='Ensalada fresca',
            ingredientes='Lechuga\nQueso\nCrutones',
            instrucciones='Mezclar ingredientes',
            tiempo_preparacion=15,
            porciones=2,
            dificultad='facil',
            categoria=self.categoria,
            creador=self.user
        )
        
        # Buscar por título
        url = reverse('recetas:api:receta-list')
        response = self.client.get(url, {'search': 'chocolate'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['titulo'], 'Torta de Chocolate')
    
    def test_receta_category_filter(self):
        """Test filtro por categoría en API."""
        # Crear otra categoría y receta
        categoria2 = Categoria.objects.create(
            nombre='Ensaladas',
            descripcion='Recetas de ensaladas'
        )
        
        Receta.objects.create(
            titulo='Ensalada César',
            descripcion='Ensalada fresca',
            ingredientes='Lechuga\nQueso\nCrutones',
            instrucciones='Mezclar ingredientes',
            tiempo_preparacion=15,
            porciones=2,
            dificultad='facil',
            categoria=categoria2,
            creador=self.user
        )
        
        # Filtrar por categoría
        url = reverse('recetas:api:receta-list')
        response = self.client.get(url, {'categoria': self.categoria.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['titulo'], 'Torta de Chocolate')
    
    def test_receta_difficulty_filter(self):
        """Test filtro por dificultad en API."""
        # Crear receta con otra dificultad
        Receta.objects.create(
            titulo='Receta Fácil',
            descripcion='Una receta muy fácil',
            ingredientes='Ingrediente simple',
            instrucciones='Paso simple',
            tiempo_preparacion=15,
            porciones=2,
            dificultad='facil',
            categoria=self.categoria,
            creador=self.user
        )
        
        # Filtrar por dificultad
        url = reverse('recetas:api:receta-list')
        response = self.client.get(url, {'dificultad': 'facil'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['titulo'], 'Receta Fácil')


class CategoriaAPITest(TestCase):
    """Tests para la API de categorías."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.categoria = Categoria.objects.create(
            nombre='Postres',
            descripcion='Recetas de postres deliciosos'
        )
    
    def test_get_categorias_list(self):
        """Test GET lista de categorías."""
        url = reverse('recetas:api:categoria-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['nombre'], 'Postres')
    
    def test_get_categoria_detail(self):
        """Test GET detalle de categoría."""
        url = reverse('recetas:api:categoria-detail', kwargs={'pk': self.categoria.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['nombre'], 'Postres')
        self.assertEqual(data['descripcion'], 'Recetas de postres deliciosos')
    
    def test_create_categoria_authenticated(self):
        """Test POST crear categoría autenticado."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'nombre': 'Bebidas',
            'descripcion': 'Recetas de bebidas refrescantes'
        }
        
        url = reverse('recetas:api:categoria-list')
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categoria.objects.count(), 2)
        
        nueva_categoria = Categoria.objects.get(nombre='Bebidas')
        self.assertEqual(nueva_categoria.descripcion, 'Recetas de bebidas refrescantes')
    
    def test_create_categoria_unauthenticated(self):
        """Test POST crear categoría sin autenticación."""
        data = {
            'nombre': 'Bebidas',
            'descripcion': 'Recetas de bebidas refrescantes'
        }
        
        url = reverse('recetas:api:categoria-list')
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TagAPITest(TestCase):
    """Tests para la API de tags."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.tag = Tag.objects.create(
            nombre='Chocolate',
            descripcion='Recetas con chocolate'
        )
    
    def test_get_tags_list(self):
        """Test GET lista de tags."""
        url = reverse('recetas:api:tag-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['nombre'], 'Chocolate')
    
    def test_get_tag_detail(self):
        """Test GET detalle de tag."""
        url = reverse('recetas:api:tag-detail', kwargs={'pk': self.tag.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['nombre'], 'Chocolate')
        self.assertEqual(data['descripcion'], 'Recetas con chocolate')
    
    def test_create_tag_authenticated(self):
        """Test POST crear tag autenticado."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'nombre': 'Vegano',
            'descripcion': 'Recetas veganas'
        }
        
        url = reverse('recetas:api:tag-list')
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 2)
        
        nuevo_tag = Tag.objects.get(nombre='Vegano')
        self.assertEqual(nuevo_tag.descripcion, 'Recetas veganas')
    
    def test_create_tag_unauthenticated(self):
        """Test POST crear tag sin autenticación."""
        data = {
            'nombre': 'Vegano',
            'descripcion': 'Recetas veganas'
        }
        
        url = reverse('recetas:api:tag-list')
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
