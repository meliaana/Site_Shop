import django_filters

from shop.models import Product


class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    category__title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price', 'category', ]
