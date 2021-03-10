from django.contrib import admin
from .models import CartItem, Category, Cart, Product, Tag

admin.site.register([CartItem, Category, Cart, Product, Tag])
