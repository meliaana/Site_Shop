from ckeditor.fields import RichTextField
from django.db import models

from user.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class Product(models.Model):
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = RichTextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Tag(models.Model):
    products = models.ManyToManyField(to='Product', related_name='tags')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='cartitem')
    cart = models.ForeignKey(to='Cart', on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        price = Product.objects.get(pk=self.product.pk).price
        if not self.price:
            self.price = price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.OneToOneField(to='user.User', on_delete=models.CASCADE, default=None)
