from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Category, Product, Tag, CartItem


class TagSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    tag = serializers.CharField()

    class Meta:
        model = Tag


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', ]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField(method_name='get_tags')

    def get_tags(self, obj):
        return self.context['tag']

    class Meta:
        model = Category
        fields = ['id', 'title', 'order', 'tag']


class CategoryList(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('category',)
        lookup_field = 'slug'


class ProductCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Product
        fields = ['tags', 'category', 'title', 'slug', 'price', 'description', 'is_published', 'quantity', ]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ('cart', )
