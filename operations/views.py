from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from accounts.permissions import (
    IsActiveUser,
    IsDeliveryOrAdmin,
    IsClientOrFarmerOrAdmin,
    IsStaffOrAdmin,
)

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

@extend_schema_view(
    list=extend_schema(tags=["Admin Dashboard", "Client Dashboard", "Delivery Dashboard", "Farmer Dashboard"]),
    create=extend_schema(tags=["Client Dashboard", "Farmer Dashboard"]),
)
class OrdersViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset           = Orders.objects.all()
    serializer_class   = OrdersSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsClientOrFarmerOrAdmin]
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ["order_date", "delivery_date"]
    ordering           = ["-order_date"]
    http_method_names  = ["get", "post", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == user.ADMIN or user.is_staff:
            return Orders.objects.all().prefetch_related("items")
        return Orders.objects.filter(user=user).prefetch_related("items").order_by("-order_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─────────────────────────────────────────────
# ORDER ITEMS
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(tags=["Client Dashboard"]),
    create=extend_schema(tags=["Client Dashboard"]),
)
class OrderItemViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset           = OrderItem.objects.all()
    serializer_class   = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsClientOrFarmerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == user.ADMIN or user.is_staff:
            return OrderItem.objects.all().select_related("product", "order")
        return OrderItem.objects.filter(order__user=user).select_related("product", "order")


# ─────────────────────────────────────────────
# ORDER PAYMENTS
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(tags=["Admin Dashboard", "Client Dashboard"]),
    create=extend_schema(tags=["Client Dashboard"]),
)
class OrdersPaymentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset           = OrdersPayment.objects.all()
    serializer_class   = OrdersPaymentSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsClientOrFarmerOrAdmin]
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ["payment_date", "amount", "status"]
    ordering           = ["-payment_date"]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == user.ADMIN or user.is_staff:
            return OrdersPayment.objects.all().select_related("order")
        return OrdersPayment.objects.filter(user=user).select_related("order").order_by("-payment_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─────────────────────────────────────────────
# SUBSCRIPTIONS
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(tags=["Admin Dashboard", "Client Dashboard", "Delivery Dashboard"]),
    create=extend_schema(tags=["Client Dashboard"]),
)
class SubscriptionsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset           = Subscriptions.objects.all()
    serializer_class   = SubscriptionsSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsClientOrFarmerOrAdmin]
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ["start_date", "status", "frequency"]
    ordering           = ["-start_date"]
    http_method_names  = ["get", "post", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == user.ADMIN or user.is_staff:
            return Subscriptions.objects.all().prefetch_related("items")
        return Subscriptions.objects.filter(user=user).prefetch_related("items").order_by("-start_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─────────────────────────────────────────────
# SUBSCRIPTION ITEMS
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(tags=["Client Dashboard"]),
    create=extend_schema(tags=["Client Dashboard"]),
)
class SubscriptionItemViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset           = SubscriptionItem.objects.all()
    serializer_class   = SubscriptionItemSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsClientOrFarmerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == user.ADMIN or user.is_staff:
            return SubscriptionItem.objects.all().select_related("product", "subscription")
        return SubscriptionItem.objects.filter(
            subscription__user=user
        ).select_related("product", "subscription")


# ─────────────────────────────────────────────
# SUBSCRIPTION PAYMENTS
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(tags=["Admin Dashboard", "Client Dashboard"]),
    create=extend_schema(tags=["Client Dashboard"]),
)
class SubscriptionPaymentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset           = SubscriptionPayment.objects.all()
    serializer_class   = SubscriptionPaymentSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsClientOrFarmerOrAdmin]
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ["payment_date", "amount", "status"]
    ordering           = ["-payment_date"]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == user.ADMIN or user.is_staff:
            return SubscriptionPayment.objects.all().select_related("subscription")
        return SubscriptionPayment.objects.filter(
            user=user
        ).select_related("subscription").order_by("-payment_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─────────────────────────────────────────────
# DELIVERIES
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(tags=["Admin Dashboard", "Delivery Dashboard"]),
)
class DeliveryViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset           = Delivery.objects.all()
    serializer_class   = DeliverySerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsDeliveryOrAdmin]
    filter_backends    = [filters.OrderingFilter, filters.SearchFilter]
    search_fields      = ["status"]
    ordering_fields    = ["delivery_date", "status"]
    ordering           = ["-delivery_date"]
    http_method_names  = ["get", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == user.ADMIN or user.is_staff:
            return Delivery.objects.all().select_related("order", "delivery_address")
        return Delivery.objects.filter(user=user).select_related("order", "delivery_address")
