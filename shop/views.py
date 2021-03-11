import json

import requests
from django.db.models import Sum, F, FloatField
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .models import Category, Product, Tag, CartItem, Cart
from .serializer import CategorySerializer, ProductListSerializer, CategoryList, ProductDetailSerializer, \
    ProductCreateSerializer, CartItemSerializer, CartSerializer


def send_request(text):
    headers = {
        'Content-type': 'application/json',
    }
    url = 'https://hooks.slack.com/services/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'
    data = '{"text":"'+str(text)+'"}'
    print(data)
    response = requests.post(url=url, headers=headers, data=data)


    return response


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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
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


class CartViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_serializer_context(self):
        total_cost = CartItem.objects.filter(is_active=True, cart=self.get_object().pk).aggregate(
            price=Sum(F('price') * F('quantity'), output_field=FloatField()))
        context = {"total_cots": total_cost}
        return context

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(send_request(serializer.data))
        return Response(serializer.data)
