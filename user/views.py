from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.models import Product
from .models import User
from user.serializers import RegistrationSerializer, UserListSerializer, UserDetailSerliazer


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            return Response({'response': "successfully registered account", 'email': user.email})
        else:
            return Response(serializer.errors)


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        notes = Product.objects.filter(author=user)
        serializer = UserDetailSerliazer({'email': user.email, 'notes': notes})
        return Response(serializer.data)
