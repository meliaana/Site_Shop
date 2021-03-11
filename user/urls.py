from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserCreate, UserList, users_detail

urlpatterns = [path('register/', UserCreate.as_view(), name='register'),
               path('login/', obtain_auth_token, name='login'),
               path('', UserList.as_view(), name='all-users'),
               path('detail/<int:pk>/', users_detail, name='user-detail'),

               ]
