from rest_framework import serializers
from .models import Category, Product, Inventory, ProductInventory


# =========================
# CATEGORY
# =========================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# =========================
# PRODUCT
# =========================
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_name",
            "name",
            "description",
            "price_per_unit",
            "is_available",
            "created_at",
        ]


# =========================
# INVENTORY
# =========================
class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "product_name",
            "name",
            "current_stock",
            "updated_at",
        ]


# =========================
# PRODUCT INVENTORY
# =========================
class ProductInventorySerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "product",
            "product_name",
            "inventory",
            "transaction_type",
            "stock_before",
            "stock_after",
            "created_at",
        ]

    def create(self, validated_data):
        return ProductInventory.objects.create(**validated_data)