from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Category, Product, Tag, CartItem, Cart


class TagSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    tag = serializers.CharField()

    class Meta:
        model = Tag


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'category']


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
    product = serializers.CharField(source='product.title', read_only=True)
    price = serializers.CharField(source='product.price', read_only=True)

    class Meta:
        model = CartItem
        fields = ('quantity', 'price', 'product', 'is_active')



