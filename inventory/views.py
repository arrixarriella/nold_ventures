from drf_spectacular.utils import extend_schema, extend_schema_view
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
@extend_schema_view(
    list=extend_schema(tags=["Products"]),
    create=extend_schema(tags=["Products"]),
    retrieve=extend_schema(tags=["Products"]),
    update=extend_schema(tags=["Products"]),
    partial_update=extend_schema(tags=["Products"]),
    destroy=extend_schema(tags=["Products"]),
)
class CategoryViewSet(viewsets.ModelViewSet):
    """
    Manage product categories (Eggs, Feed, Chicks, Meat)
    """
    queryset = Category.objects.all().order_by("-created_at")
    serializer_class = CategorySerializer


# =========================
# PRODUCT VIEWSET
# =========================
@extend_schema_view(
    list=extend_schema(tags=["Products"]),
    create=extend_schema(tags=["Products"]),
    retrieve=extend_schema(tags=["Products"]),
    update=extend_schema(tags=["Products"]),
    partial_update=extend_schema(tags=["Products"]),
    destroy=extend_schema(tags=["Products"]),
)
class ProductViewSet(viewsets.ModelViewSet):
    """
    Manage poultry products
    """
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer


# =========================
# INVENTORY VIEWSET
# =========================
@extend_schema_view(
    list=extend_schema(tags=["Inventory"]),
    create=extend_schema(tags=["Inventory"]),
    retrieve=extend_schema(tags=["Inventory"]),
    update=extend_schema(tags=["Inventory"]),
    partial_update=extend_schema(tags=["Inventory"]),
    destroy=extend_schema(tags=["Inventory"]),
)
class InventoryViewSet(viewsets.ModelViewSet):
    """
    Manage stock per product
    """
    queryset = Inventory.objects.all().order_by("-updated_at")
    serializer_class = InventorySerializer


# =========================
# PRODUCT INVENTORY VIEWSET
# =========================
@extend_schema_view(
    list=extend_schema(tags=["Transactions"]),
    create=extend_schema(tags=["Transactions"]),
    retrieve=extend_schema(tags=["Transactions"]),
    update=extend_schema(tags=["Transactions"]),
    partial_update=extend_schema(tags=["Transactions"]),
    destroy=extend_schema(tags=["Transactions"]),
)
class ProductInventoryViewSet(viewsets.ModelViewSet):
    """
    Track stock movements (IN / OUT)
    """
    queryset = ProductInventory.objects.all().order_by("-created_at")
    serializer_class = ProductInventorySerializer