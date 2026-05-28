from django.contrib import admin
from .models import Category, Product, Inventory, ProductInventory


# =========================
# CATEGORY ADMIN
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)


# =========================
# PRODUCT ADMIN
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price_per_unit",
        "is_available",
        "created_at",
    )

    list_filter = ("category", "is_available")
    search_fields = ("name",)
    ordering = ("-created_at",)


# =========================
# INVENTORY ADMIN
# =========================
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "name",
        "current_stock",
        "updated_at",
    )

    list_filter = ("updated_at",)
    search_fields = ("product__name",)
    ordering = ("-updated_at",)


# =========================
# PRODUCT INVENTORY ADMIN (STOCK MOVEMENTS)
# =========================
@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "get_category",
        "inventory",
        "transaction_type",
        "stock_before",
        "stock_after",
        "created_at",
    )

    list_filter = ("transaction_type", "product__category")

    readonly_fields = (
        "stock_before",
        "stock_after",
        "created_at",
    )

    def get_category(self, obj):
        return obj.product.category.name

    get_category.short_description = "Category"