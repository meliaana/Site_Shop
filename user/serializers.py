from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shop.models import Cart
from shop.serializer import CartItemSerializer
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


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, obj):
        return self.context['total_cots']

    class Meta:
        model = Cart
        fields = ['items', 'total_price']

