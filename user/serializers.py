from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password2 != password:
            raise ValidationError({'password': 'Passwords must match'})
        user.set_password(password)
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'email']


class UserDetailSerliazer(serializers.Serializer):
    email = serializers.EmailField()
    cart = serializers.StringRelatedField(many=True)


