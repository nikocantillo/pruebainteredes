from http import client
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'administrd@meta.com',
            password = 'password'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="prueba@meta.com",
            password='pasword',
            user_name="prueba nombre completo"
        )

    def test_users_listed(self):
        """verificar si los usuarios estan enlistados"""

        url = reverse('admin:users_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.user_name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """prueba que la pagina que el usuario edita funcione"""
        url = reverse('admin:users_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


    def test_create_user_page(self):
        """prueba que la pagina de crear funcione"""
        url = reverse('admin:users_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)



