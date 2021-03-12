import requests
from django.db.models import Sum, F, FloatField
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from Site_Shop.local_settings import slack_hook
from shop.models import Cart, CartItem
from user.serializers import RegistrationSerializer, UserListSerializer, UserDetailSerliazer, CartSerializer
from .models import User


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
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        cart = Cart.objects.get(owner=request.user)
        total_cost = CartItem.objects.filter(is_active=True, cart=cart).aggregate(
            price=Sum(F('price') * F('quantity'), output_field=FloatField()))
        context = {"total_cots": total_cost['price']}
        serializer = CartSerializer(cart, context=context)
        return Response(serializer.data)


class BuyView():
    permission_classes = [IsAuthenticated, ]
    # @TODO
    #buy
    #save_data in history
    #send_slack_message


def send_slack_message(text):
    headers = {
        'Content-type': 'application/json',
    }
    url = slack_hook
    data = '{"text":"' + str(text) + '"}'
    response = requests.post(url=url, headers=headers, data=data)

    return response
