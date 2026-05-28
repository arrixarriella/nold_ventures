from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsActiveUser

from .models import (
    Orders,
    OrderItem,
    OrdersPayment,
    Subscriptions,
    SubscriptionItem,
    SubscriptionPayment,
    Delivery,
)
from .serializers import (
    OrdersSerializer,
    OrderItemSerializer,
    OrdersPaymentSerializer,
    SubscriptionsSerializer,
    SubscriptionItemSerializer,
    SubscriptionPaymentSerializer,
    DeliverySerializer,
)


# ─────────────────────────────────────────────
# ORDERS
# ─────────────────────────────────────────────

class OrdersViewSet(viewsets.ModelViewSet):
    """
    GET    /api/orders/          → list logged-in user's orders
    POST   /api/orders/          → create a new order
    GET    /api/orders/<id>/     → retrieve a single order
    PUT    /api/orders/<id>/     → full update
    PATCH  /api/orders/<id>/     → partial update
    DELETE /api/orders/<id>/     → delete
    """
    serializer_class   = OrdersSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ["order_date", "delivery_date"]
    ordering           = ["-order_date"]

    def get_queryset(self):
        return Orders.objects.filter(
            user=self.request.user
        ).prefetch_related("items").order_by("-order_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─────────────────────────────────────────────
# ORDER ITEMS
# ─────────────────────────────────────────────

class OrderItemViewSet(viewsets.ModelViewSet):
    """
    GET    /api/order-items/          → list items for logged-in user's orders
    POST   /api/order-items/          → add item to an order
    GET    /api/order-items/<id>/     → retrieve a single item
    PUT    /api/order-items/<id>/     → full update
    PATCH  /api/order-items/<id>/     → partial update
    DELETE /api/order-items/<id>/     → delete
    """
    serializer_class   = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]

    def get_queryset(self):
        return OrderItem.objects.filter(
            order__user=self.request.user
        ).select_related("product", "order")


# ─────────────────────────────────────────────
# ORDER PAYMENTS
# ─────────────────────────────────────────────

class OrdersPaymentViewSet(viewsets.ModelViewSet):
    """
    GET    /api/order-payments/          → list logged-in user's order payments
    POST   /api/order-payments/          → create a payment for an order
    GET    /api/order-payments/<id>/     → retrieve a single payment
    PUT    /api/order-payments/<id>/     → full update
    PATCH  /api/order-payments/<id>/     → partial update
    DELETE /api/order-payments/<id>/     → delete
    """
    serializer_class   = OrdersPaymentSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ["payment_date", "amount", "status"]
    ordering           = ["-payment_date"]

    def get_queryset(self):
        # ✅ Users only see their own payments
        return OrdersPayment.objects.filter(
            user=self.request.user
        ).select_related("order").order_by("-payment_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─────────────────────────────────────────────
# SUBSCRIPTIONS
# ─────────────────────────────────────────────

class SubscriptionsViewSet(viewsets.ModelViewSet):
    """
    GET    /api/subscriptions/          → list logged-in user's subscriptions
    POST   /api/subscriptions/          → create a new subscription
    GET    /api/subscriptions/<id>/     → retrieve a single subscription
    PUT    /api/subscriptions/<id>/     → full update
    PATCH  /api/subscriptions/<id>/     → partial update
    DELETE /api/subscriptions/<id>/     → delete
    """
    serializer_class   = SubscriptionsSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ["start_date", "status", "frequency"]
    ordering           = ["-start_date"]

    def get_queryset(self):
        return Subscriptions.objects.filter(
            user=self.request.user
        ).prefetch_related("items").order_by("-start_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─────────────────────────────────────────────
# SUBSCRIPTION ITEMS
# ─────────────────────────────────────────────

class SubscriptionItemViewSet(viewsets.ModelViewSet):
    """
    GET    /api/subscription-items/          → list items for logged-in user's subscriptions
    POST   /api/subscription-items/          → add item to a subscription
    GET    /api/subscription-items/<id>/     → retrieve a single item
    PUT    /api/subscription-items/<id>/     → full update
    PATCH  /api/subscription-items/<id>/     → partial update
    DELETE /api/subscription-items/<id>/     → delete
    """
    serializer_class   = SubscriptionItemSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]

    def get_queryset(self):
        return SubscriptionItem.objects.filter(
            subscription__user=self.request.user
        ).select_related("product", "subscription")


# ─────────────────────────────────────────────
# SUBSCRIPTION PAYMENTS
# ─────────────────────────────────────────────

class SubscriptionPaymentViewSet(viewsets.ModelViewSet):
    """
    GET    /api/subscription-payments/          → list logged-in user's subscription payments
    POST   /api/subscription-payments/          → create a payment for a subscription
    GET    /api/subscription-payments/<id>/     → retrieve a single payment
    PUT    /api/subscription-payments/<id>/     → full update
    PATCH  /api/subscription-payments/<id>/     → partial update
    DELETE /api/subscription-payments/<id>/     → delete
    """
    serializer_class   = SubscriptionPaymentSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ["payment_date", "amount", "status"]
    ordering           = ["-payment_date"]

    def get_queryset(self):
        return SubscriptionPayment.objects.filter(
            user=self.request.user
        ).select_related("subscription").order_by("-payment_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─────────────────────────────────────────────
# DELIVERY
# ─────────────────────────────────────────────

class DeliveryViewSet(viewsets.ModelViewSet):
    """
    GET    /api/deliveries/          → list logged-in user's deliveries
    POST   /api/deliveries/          → create a delivery
    GET    /api/deliveries/<id>/     → retrieve a single delivery
    PUT    /api/deliveries/<id>/     → full update
    PATCH  /api/deliveries/<id>/     → partial update
    DELETE /api/deliveries/<id>/     → delete
    """
    serializer_class   = DeliverySerializer
    permission_classes = [IsAuthenticated, IsActiveUser]
    filter_backends    = [filters.OrderingFilter, filters.SearchFilter]
    search_fields      = ["status"]
    ordering_fields    = ["delivery_date", "status"]
    ordering           = ["-delivery_date"]

    def get_queryset(self):
        return Delivery.objects.filter(
            user=self.request.user
        ).select_related(
            "order", "delivery_address"
        ).order_by("-delivery_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)