from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serializando un objeto usuario"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'user_name')
        extra_kwargs = {'password':{'write_only': True, 'min_length': 5}}

    def create(self, validate_date):
        """crear usuario con clave enciptada"""
        return get_user_model().objects.create_user(**validate_date)

    def update(self, instance, validated_data):
        """actualizar usuario"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """autenticacion del usuario"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """validar y autenticar el usuario"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            msg = _('no es posible autenticar con las credenciales dadas')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        
        return attrs

