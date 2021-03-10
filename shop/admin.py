from django.contrib import admin
from .models import CartItem, Category, Cart, Product

admin.site.register([CartItem, Category, Cart, Product])
