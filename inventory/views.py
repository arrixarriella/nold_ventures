from rest_framework import viewsets
from .models import Category, Product, Inventory, ProductInventory
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    InventorySerializer,
    ProductInventorySerializer
)


# =========================
# CATEGORY VIEWSET
# =========================
class CategoryViewSet(viewsets.ModelViewSet):
    """
    Manage product categories (Eggs, Feed, Chicks, Meat)
    """
    queryset = Category.objects.all().order_by("-created_at")
    serializer_class = CategorySerializer


# =========================
# PRODUCT VIEWSET
# =========================
class ProductViewSet(viewsets.ModelViewSet):
    """
    Manage poultry products
    """
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer


# =========================
# INVENTORY VIEWSET
# =========================
class InventoryViewSet(viewsets.ModelViewSet):
    """
    Manage stock per product
    """
    queryset = Inventory.objects.all().order_by("-updated_at")
    serializer_class = InventorySerializer


# =========================
# PRODUCT INVENTORY VIEWSET
# =========================
class ProductInventoryViewSet(viewsets.ModelViewSet):
    """
    Track stock movements (IN / OUT)
    """
    queryset = ProductInventory.objects.all().order_by("-created_at")
    serializer_class = ProductInventorySerializer