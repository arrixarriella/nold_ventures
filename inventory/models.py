from django.db import models


# =========================
# CATEGORY
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


# =========================
# PRODUCT
# =========================
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=200)
    description = models.TextField()

    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


# =========================
# INVENTORY
# =========================
class Inventory(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory"
    )

    name = models.CharField(max_length=200)
    current_stock = models.PositiveIntegerField()

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} stock"

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventory"


# =========================
# PRODUCT INVENTORY
# =========================
class ProductInventory(models.Model):

    TRANSACTION_TYPES = (
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=3,
        choices=TRANSACTION_TYPES
    )

    stock_before = models.PositiveIntegerField()
    stock_after = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        current_stock = self.inventory.current_stock

        # current stock before transaction
        self.stock_before = current_stock

        # stock increase
        if self.transaction_type == "IN":
            self.stock_after = current_stock + 1
            self.inventory.current_stock = current_stock + 1

        # stock decrease
        elif self.transaction_type == "OUT":
            self.stock_after = current_stock - 1
            self.inventory.current_stock = current_stock - 1

        # save updated inventory
        self.inventory.save()

        # save transaction
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.transaction_type}"

    class Meta:
        verbose_name = "Product Inventory"
        verbose_name_plural = "Product Inventories"