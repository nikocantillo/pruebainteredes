from user import serializers
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
    """crear nuevo usuario"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """creando un nuevo token para usuario"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """manejar el usuario autenticado"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permissions_classes =(permissions.IsAuthenticated,)

    def get_object(self):
        """obtener y retornar el usuario authenticado"""
        return self.request.user