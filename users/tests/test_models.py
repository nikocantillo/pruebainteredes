from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    
    def test_user_create_with_email_success(self):
        """conrreo y contraseña correcta"""
        email = 'canvarSDFSogy@gmail.com'
        password = "Testpass345"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ test nuevo usuario normalizado"""
        email = 'canvarSDFSogy@gmail.com'
        user = get_user_model().objects.create_user(email, "Testpass123")

        self.assertEqual(user.email, email)

    def test_new_user_invalid_email(self):
        """email invalido"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'canvarSDFSogy@gmail.com')


    def test_create_new_superuser(self):
        """prueba super usuario creado"""
        email = 'canvarSDFSogy@gmail.com'
        password = "Testpass345"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

