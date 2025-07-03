from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from recetas.models import Receta, Categoria, Tag
import json


class RecetaViewTest(TestCase):
    """Tests para las vistas de recetas."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.client = Client()
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
    
    def test_index_view(self):
        """Test de la vista índice."""
        response = self.client.get(reverse('recetas:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recetas Gourmet')
        self.assertContains(response, 'Descubre sabores únicos')
    
    def test_lista_view(self):
        """Test de la vista lista de recetas."""
        response = self.client.get(reverse('recetas:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Torta de Chocolate')
        self.assertContains(response, 'Todas las Recetas')
    
    def test_detalle_view(self):
        """Test de la vista detalle de receta."""
        response = self.client.get(reverse('recetas:detalle', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Torta de Chocolate')
        self.assertContains(response, 'Una deliciosa torta de chocolate')
        self.assertContains(response, 'Chocolate')
        self.assertContains(response, 'Huevos')
    
    def test_crear_view_get(self):
        """Test GET de la vista crear receta."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recetas:crear'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nueva Receta')
    
    def test_crear_view_post(self):
        """Test POST de la vista crear receta."""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'titulo': 'Nueva Receta',
            'descripcion': 'Descripción de la nueva receta',
            'ingredientes': 'Ingrediente 1\nIngrediente 2',
            'instrucciones': 'Paso 1\nPaso 2',
            'tiempo_preparacion': 30,
            'porciones': 4,
            'dificultad': 'facil',
            'categoria': self.categoria.id,
        }
        
        response = self.client.post(reverse('recetas:crear'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        
        # Verificar que la receta se creó
        nueva_receta = Receta.objects.get(titulo='Nueva Receta')
        self.assertEqual(nueva_receta.creador, self.user)
        self.assertEqual(nueva_receta.categoria, self.categoria)
    
    def test_editar_view_get(self):
        """Test GET de la vista editar receta."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recetas:editar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editar Receta')
        self.assertContains(response, 'Torta de Chocolate')
    
    def test_editar_view_post(self):
        """Test POST de la vista editar receta."""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'titulo': 'Torta de Chocolate Modificada',
            'descripcion': 'Descripción modificada',
            'ingredientes': 'Chocolate\nHuevos\nHarina\nAzúcar\nVainilla',
            'instrucciones': 'Mezclar ingredientes\nHornear 45 minutos\nDejar enfriar',
            'tiempo_preparacion': 75,
            'porciones': 10,
            'dificultad': 'dificil',
            'categoria': self.categoria.id,
        }
        
        response = self.client.post(reverse('recetas:editar', kwargs={'pk': self.receta.id}), form_data)
        self.assertEqual(response.status_code, 302)  # Redirección después de editar
        
        # Verificar que la receta se modificó
        receta_modificada = Receta.objects.get(id=self.receta.id)
        self.assertEqual(receta_modificada.titulo, 'Torta de Chocolate Modificada')
        self.assertEqual(receta_modificada.tiempo_preparacion, 75)
    
    def test_eliminar_view_get(self):
        """Test GET de la vista eliminar receta."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recetas:eliminar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '¿Eliminar Receta?')
        self.assertContains(response, 'Torta de Chocolate')
    
    def test_eliminar_view_post(self):
        """Test POST de la vista eliminar receta."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('recetas:eliminar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        
        # Verificar que la receta se eliminó
        with self.assertRaises(Receta.DoesNotExist):
            Receta.objects.get(id=self.receta.id)
    
    def test_favoritos_view_anonymous(self):
        """Test de la vista favoritos sin usuario autenticado."""
        response = self.client.get(reverse('recetas:favoritos'))
        self.assertEqual(response.status_code, 302)  # Redirección a login
    
    def test_favoritos_view_authenticated(self):
        """Test de la vista favoritos con usuario autenticado."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recetas:favoritos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mis Favoritos')
    
    def test_busqueda_view(self):
        """Test de la vista de búsqueda."""
        response = self.client.get(reverse('recetas:busqueda'), {'q': 'chocolate'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultados de búsqueda')
    
    def test_busqueda_ajax(self):
        """Test de búsqueda AJAX."""
        response = self.client.get(
            reverse('recetas:busqueda_ajax'),
            {'q': 'chocolate'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertIn('resultados', data)
        self.assertTrue(len(data['resultados']) > 0)
    
    def test_toggle_favorito_ajax(self):
        """Test de toggle favorito AJAX."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('recetas:toggle_favorito'),
            {'receta_id': self.receta.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertIn('favorito', data)
        self.assertIn('total_favoritos', data)
    
    def test_receta_access_control(self):
        """Test de control de acceso a recetas."""
        # Crear otro usuario
        User.objects.create_user(
            username='otrouser',
            email='otro@example.com',
            password='testpass123'
        )
        
        # Intentar editar receta de otro usuario
        self.client.login(username='otrouser', password='testpass123')
        response = self.client.get(reverse('recetas:editar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_receta_search_filters(self):
        """Test de filtros de búsqueda."""
        # Crear receta con diferentes características
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
        response = self.client.get(reverse('recetas:lista'), {'dificultad': 'facil'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Receta Fácil')
        self.assertNotContains(response, 'Torta de Chocolate')
        
        # Filtrar por tiempo máximo
        response = self.client.get(reverse('recetas:lista'), {'tiempo_max': 30})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Receta Fácil')
        self.assertNotContains(response, 'Torta de Chocolate')
    
    def test_receta_pagination(self):
        """Test de paginación de recetas."""
        # Crear muchas recetas para probar paginación
        for i in range(15):
            Receta.objects.create(
                titulo=f'Receta {i}',
                descripcion=f'Descripción {i}',
                ingredientes=f'Ingrediente {i}',
                instrucciones=f'Paso {i}',
                tiempo_preparacion=30,
                porciones=4,
                dificultad='facil',
                categoria=self.categoria,
                creador=self.user
            )
        
        # Primera página
        response = self.client.get(reverse('recetas:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Página 1')
        
        # Segunda página
        response = self.client.get(reverse('recetas:lista'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Página 2')


class RecetaPermissionTest(TestCase):
    """Tests para permisos de recetas."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        
        self.categoria = Categoria.objects.create(
            nombre='Postres',
            descripcion='Recetas de postres deliciosos'
        )
        
        self.receta = Receta.objects.create(
            titulo='Receta del Usuario 1',
            descripcion='Receta creada por el usuario 1',
            ingredientes='Ingrediente 1\nIngrediente 2',
            instrucciones='Paso 1\nPaso 2',
            tiempo_preparacion=30,
            porciones=4,
            dificultad='facil',
            categoria=self.categoria,
            creador=self.user1
        )
    
    def test_crear_receta_sin_autenticacion(self):
        """Test crear receta sin autenticación."""
        response = self.client.get(reverse('recetas:crear'))
        self.assertEqual(response.status_code, 302)  # Redirección a login
    
    def test_editar_receta_sin_autenticacion(self):
        """Test editar receta sin autenticación."""
        response = self.client.get(reverse('recetas:editar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 302)  # Redirección a login
    
    def test_eliminar_receta_sin_autenticacion(self):
        """Test eliminar receta sin autenticación."""
        response = self.client.get(reverse('recetas:eliminar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 302)  # Redirección a login
    
    def test_editar_receta_usuario_incorrecto(self):
        """Test editar receta de otro usuario."""
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('recetas:editar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_eliminar_receta_usuario_incorrecto(self):
        """Test eliminar receta de otro usuario."""
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('recetas:eliminar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_editar_receta_usuario_correcto(self):
        """Test editar receta del usuario propietario."""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('recetas:editar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_eliminar_receta_usuario_correcto(self):
        """Test eliminar receta del usuario propietario."""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('recetas:eliminar', kwargs={'pk': self.receta.id}))
        self.assertEqual(response.status_code, 200)
