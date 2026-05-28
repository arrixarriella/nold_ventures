from django.db import models
from django.utils import timezone
from accounts.models import User, UserAddress
from inventory.models import Product


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateField()

    def __str__(self):
        return f"Order #{self.id} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product} x {self.quantity}"


class OrdersPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("mobile_money", "Mobile Money"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.amount = sum(
            item.quantity * item.product.price
            for item in self.order.items.all()
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderPayment #{self.id}"


class Subscriptions(models.Model):
    FREQUENCY_CHOICES = [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("expired", "Expired"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Subscription #{self.id} - {self.user}"


class SubscriptionItem(models.Model):
    subscription = models.ForeignKey(Subscriptions, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product} x {self.quantity}"


class SubscriptionPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("mobile_money", "Mobile Money"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    subscription = models.ForeignKey(Subscriptions, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.amount = sum(
            item.quantity * item.product.price
            for item in self.subscription.items.all()
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SubscriptionPayment #{self.id}"


class Delivery(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"),
    ]

    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="deliveries")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(UserAddress, on_delete=models.PROTECT)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    delivery_date = models.DateField()

    def __str__(self):
        return f"Delivery #{self.id} - Order {self.order.id}"