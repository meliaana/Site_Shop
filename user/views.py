from django.db.models import Sum, F, FloatField
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    RetrieveAPIView, ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Product, Cart, CartItem
from .models import User
from user.serializers import RegistrationSerializer, UserListSerializer, UserDetailSerliazer, CartSerializer


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'response': "successfully registered account", 'email': user.email})
        else:
            return Response(serializer.errors)


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_permissions(self):
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        cart = Cart.objects.filter(owner=user)
        serializer = UserDetailSerliazer({'email': user.email, 'cart': cart})
        return Response(serializer.data)


class CartView(APIView):

    def get(self, request):
        cart = Cart.objects.get(owner=request.user)
        total_cost = CartItem.objects.filter(is_active=True, cart=cart).aggregate(
            price=Sum(F('price') * F('quantity'), output_field=FloatField()))
        context = {"total_cots": total_cost['price']}
        print(CartItem.objects.filter(cart__owner_id=request.user.pk))
        serializer = CartSerializer(cart, context=context)
        return Response(serializer.data)


