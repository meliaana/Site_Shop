from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView, ProductViewSet, CategoryListView

router = DefaultRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
]
