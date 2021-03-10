from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Category, Product, Tag
from .serializer import CategorySerializer, ProductListSerializer, CategoryList, ProductDetailSerializer


class CategoryView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tag'] = []
        tags = Tag.objects.filter(products__category=self.get_object().pk)
        for t in tags:
            context['tag'].append(t.title)
        return context


class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryList


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def retrieve(self, request, *args, **kwargs):
        # self.lookup_field = 'slug'
        instance = self.get_object()
        serializer = ProductDetailSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        return super().create(request, *args, **kwargs)
