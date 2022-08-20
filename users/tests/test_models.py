from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    
    def test_user_create_with_email_success(self):
        """conrreo y contraseña correcta"""
        email = 'canvarecology@gmail.com'
        password = "Testpass345"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
