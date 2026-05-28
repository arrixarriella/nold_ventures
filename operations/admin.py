from django.contrib import admin
from .models import (
    Orders,
    OrderItem,
    OrdersPayment,
    Subscriptions,
    SubscriptionItem,
    SubscriptionPayment,
    Delivery,
)


# ─────────────────────────────────────────────
# INLINES
# ─────────────────────────────────────────────

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrdersPaymentInline(admin.TabularInline):
    model = OrdersPayment
    extra = 0
    readonly_fields = ("amount",)


class DeliveryInline(admin.TabularInline):
    model = Delivery
    extra = 0


class SubscriptionItemInline(admin.TabularInline):
    model = SubscriptionItem
    extra = 1


class SubscriptionPaymentInline(admin.TabularInline):
    model = SubscriptionPayment
    extra = 0
    readonly_fields = ("amount",)


# ─────────────────────────────────────────────
# ORDERS
# ─────────────────────────────────────────────

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "order_date", "delivery_date")
    list_filter = ("order_date",)
    search_fields = ("user__email", "user__full_name")
    ordering = ("-order_date",)
    inlines = [OrderItemInline, OrdersPaymentInline, DeliveryInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity")
    list_filter = ("product",)
    search_fields = ("order__id",)


@admin.register(OrdersPayment)
class OrdersPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "user", "amount", "payment_method", "status", "payment_date")
    list_filter = ("payment_method", "status", "payment_date")
    readonly_fields = ("amount",)
    search_fields = ("order__id", "user__email", "user__full_name")
    ordering = ("-payment_date",)


# ─────────────────────────────────────────────
# SUBSCRIPTIONS
# ─────────────────────────────────────────────

@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "frequency", "status", "start_date")
    list_filter = ("frequency", "status")
    search_fields = ("user__email", "user__full_name")
    ordering = ("-start_date",)
    inlines = [SubscriptionItemInline, SubscriptionPaymentInline]


@admin.register(SubscriptionItem)
class SubscriptionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "subscription", "product", "quantity")
    list_filter = ("product",)
    search_fields = ("subscription__id",)


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "subscription", "user", "amount", "payment_method", "status", "payment_date")
    list_filter = ("payment_method", "status", "payment_date")
    readonly_fields = ("amount",)
    search_fields = ("subscription__id", "user__email", "user__full_name")
    ordering = ("-payment_date",)


# ─────────────────────────────────────────────
# DELIVERY
# ─────────────────────────────────────────────

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "user", "delivery_address", "status", "delivery_date")
    list_filter = ("status", "delivery_date")
    search_fields = ("order__id", "user__email", "user__full_name")
    ordering = ("-delivery_date",)