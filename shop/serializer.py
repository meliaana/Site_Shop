from rest_framework import serializers

from .models import Category, Product, Tag


class TagSerializer(serializers.ModelSerializer):
    tag = serializers.ListField()

    class Meta:
        model = Tag
        fields = ['title']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', ]


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
