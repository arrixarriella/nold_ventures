from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from accounts.permissions import IsActiveUser, IsStaffOrAdmin

from .models import Category, Product, Inventory, ProductInventory
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    InventorySerializer,
    ProductInventorySerializer,
)


@extend_schema_view(
    list=extend_schema(tags=["Farmer Dashboard"]),
    retrieve=extend_schema(exclude=True),
)
class CategoryViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset           = Category.objects.all().order_by("-created_at")
    serializer_class   = CategorySerializer
    permission_classes = [IsAuthenticated, IsActiveUser]


@extend_schema_view(
    list=extend_schema(tags=["Client Dashboard", "Farmer Dashboard"]),
)
class ProductViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset           = Product.objects.filter(is_available=True).order_by("-created_at")
    serializer_class   = ProductSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]


@extend_schema_view(
    list=extend_schema(tags=["Admin Dashboard"]),
)
class InventoryViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset           = Inventory.objects.all().order_by("-updated_at")
    serializer_class   = InventorySerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsStaffOrAdmin]


@extend_schema_view(
    list=extend_schema(tags=["Admin Dashboard"]),
    create=extend_schema(tags=["Admin Dashboard"]),
)
class ProductInventoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset           = ProductInventory.objects.all().order_by("-created_at")
    serializer_class   = ProductInventorySerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsStaffOrAdmin]
