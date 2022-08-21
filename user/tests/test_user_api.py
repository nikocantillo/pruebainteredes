from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

#funcion o variable constante

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

#separando test entre public and private
class PublicUserApiTests(TestCase):
    """prubea api"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """usuario payload exitoso"""
        payload = {
            'email': 'test@meta.com',
            'password': 'passprueba',
            'user_name': 'nombre prueba'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exits(self):
        """si un usuario existe"""
        payload = {
            'email': 'test@meta.com',
            'password': 'passprueba',
            'user_name': 'nombre prueba',
        }

        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,)

    def test_password_too_short(self):
        """si una pass es muy corta"""
        payload = {
            'email': 'test@meta.com',
            'password': 'passprueba',
            
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,)

        user_exits = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exits)

    def test_create_token_for_user(self):
        """asegura que el token sea creado por el usuario"""
        payload = {
            'email': 'test@meta.com',
            'password': 'passprueba',
            'user_name': 'nombre prueba',
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """verificar que el token no sea creado con credeciales invalidas"""
        create_user(email='test@meta.com', password= 'passprueba',)
        payload = {
            'email':'test@meta.com',
            'password': 'mal',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """prueba si no exite el usuario que no se cree el token"""
        payload = {
            'email': 'test@meta.com',
            'password': 'passprueba',
            'user_name': 'nombre prueba',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """probar que la pass y el email sean requeridos"""
        response = self.client.post(TOKEN_URL, {'email': 'one', 'password':''})
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class PrivateUserAPiTests(TestCase):
    """prueba la api en privado"""
    def setUp(self):
        self.user = create_user(
            email = 'test@meta.com',
            password = 'passprueba',
            user_name= 'nombre prueba',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """probar obtener perfil para usuario con login"""
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'user_name': self.user.user_name,
            'email': self.user.email 
        })

    def test_post_me_not_allowed(self):
        """prueba que el post no sea permitido"""
        response = self.client.post(ME_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """probar que el usuario si esta autenticado lo deje actualizar"""
        payload = {'user_name': 'new_name', 'password': 'newpass'}
        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.user_name, payload['user_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
