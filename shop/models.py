from django.db import models
from djrichtextfield.models import RichTextField


class Category(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()


class Product(models.Model):
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='product')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = RichTextField()
    is_published = models.BooleanField(default=False)


class Tag(models.Model):
    products = models.ManyToManyField(to='Product', related_name='tag')
    title = models.CharField(max_length=255)


class CartItem(models.Model):
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='cartitem')
    cart = models.ForeignKey(to='Cart', on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    # order =
    is_active = models.BooleanField()


class Cart(models.Model):
    pass
    #owner = models.OneToOneField(to='User', on_delete=models.CASCADE)



