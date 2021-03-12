from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserCreate, UserList, users_detail, CartView

urlpatterns = [path('register/', UserCreate.as_view(), name='register'),
               path('login/', obtain_auth_token, name='login'),
               path('', UserList.as_view(), name='all-users'),
               path('<int:pk>/', users_detail, name='user-detail'),
               path('cart/', CartView.as_view(), name='cart')
               ]
