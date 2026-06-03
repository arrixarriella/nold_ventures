from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductViewSet,
    InventoryViewSet,
    ProductInventoryViewSet
)


router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'transactions', ProductInventoryViewSet, basename='productinventory')


urlpatterns = [
    path('', include(router.urls)),
]