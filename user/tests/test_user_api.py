from http import client
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

#funcion o variable constante

CREATE_USER_URL = reverse('user:create')

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
        }

        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """si una pass es muy corta"""
        payload = {
            'email': 'test@meta.com',
            'password': 'passprueba',
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_exits = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exits)

