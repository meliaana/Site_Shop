from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .filters import ProductFilter
from .models import Category, Product, Tag, CartItem, Cart
from .serializer import CategorySerializer, ProductListSerializer, CategoryList, ProductDetailSerializer, \
    ProductCreateSerializer, CartItemSerializer


class CategoryView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tag'] = []
        tags = Tag.objects.filter(products__category=self.get_object().pk).distinct()
        for t in tags:
            context['tag'].append(t.title)
        return context


class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryList


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    serializer_action_class = {'list': ProductListSerializer,
                               'retrieve': ProductDetailSerializer,
                               'create': ProductCreateSerializer,
                               'update': ProductCreateSerializer,
                               'add_to_cart': CartItemSerializer}
    filterset_class = ProductFilter


    # lookup_field = 'slug'

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        try:
            return self.serializer_action_class[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            prod = Product.objects.get(pk=pk)
            quantity = serializer.data['quantity']
            if prod.quantity < quantity:
                return Response({'status': 'Not enough product'})
            cart_item = CartItem(
                product=prod,
                cart=Cart.objects.get(pk=request.user.pk),
                is_active=serializer.data['is_active'],
                quantity=quantity,
            )
            cart_item.save()
            prod.quantity -= quantity
            prod.save()
            return Response({'status': 'created'})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
