from rest_framework import serializers
from .models import (
    Orders,
    OrderItem,
    OrdersPayment,
    Subscriptions,
    SubscriptionItem,
    SubscriptionPayment,
    Delivery,
)
from accounts.models import UserAddress
from accounts.serializers import UserSerializer
from inventory.models import Product


# ─────────────────────────────────────────────
# ORDER ITEM
# ─────────────────────────────────────────────

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model  = OrderItem
        fields = ["id", "order", "product", "quantity"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


# ─────────────────────────────────────────────
# ORDER
# ─────────────────────────────────────────────

class OrdersSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_details = UserSerializer(source="user", read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model  = Orders
        fields = [
            "id",
            "user",
            "user_details",
            "order_date",
            "delivery_date",
            "items",
        ]
        read_only_fields = ["id", "order_date"]

    def validate_delivery_date(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Delivery date cannot be in the past.")
        return value


# ─────────────────────────────────────────────
# ORDER PAYMENT
# ─────────────────────────────────────────────

class OrdersPaymentSerializer(serializers.ModelSerializer):

    amount = serializers.ReadOnlyField()
    user_details = UserSerializer(source="user", read_only=True)

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model  = OrdersPayment
        fields = [
            "id",
            "order",
            "user",
            "user_details",
            "amount",
            "payment_method",
            "status",
            "payment_date",
        ]
        read_only_fields = ["id", "amount", "payment_date"]

    def validate(self, data):
        request = self.context.get("request")
        if request and data.get("order"):
            if data["order"].user != request.user:
                raise serializers.ValidationError(
                    {"order": "You can only pay for your own orders."}
                )
        return data


# ─────────────────────────────────────────────
# SUBSCRIPTION ITEM
# ─────────────────────────────────────────────

class SubscriptionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model  = SubscriptionItem
        fields = ["id", "subscription", "product", "quantity"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


# ─────────────────────────────────────────────
# SUBSCRIPTION
# ─────────────────────────────────────────────

class SubscriptionsSerializer(serializers.ModelSerializer):

    items = SubscriptionItemSerializer(many=True, read_only=True)

    user_details = UserSerializer(source="user", read_only=True)

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model  = Subscriptions
        fields = [
            "id",
            "user",
            "user_details",
            "frequency",
            "start_date",
            "status",
            "items",
        ]
        read_only_fields = ["id"]

    def validate_start_date(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value


# ─────────────────────────────────────────────
# SUBSCRIPTION PAYMENT
# ─────────────────────────────────────────────

class SubscriptionPaymentSerializer(serializers.ModelSerializer):

    amount = serializers.ReadOnlyField()

    user_details = UserSerializer(source="user", read_only=True)


    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model  = SubscriptionPayment
        fields = [
            "id",
            "subscription",
            "user",
            "user_details",
            "amount",
            "payment_method",
            "status",
            "payment_date",
        ]
        read_only_fields = ["id", "amount", "payment_date"]

    def validate(self, data):
        request = self.context.get("request")
        if request and data.get("subscription"):
            if data["subscription"].user != request.user:
                raise serializers.ValidationError(
                    {"subscription": "You can only pay for your own subscriptions."}
                )
        return data


# ─────────────────────────────────────────────
# DELIVERY
# ─────────────────────────────────────────────

class DeliverySerializer(serializers.ModelSerializer):

    user_details = UserSerializer(source="user", read_only=True)

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model  = Delivery
        fields = [
            "id",
            "order",
            "user",
            "user_details",
            "delivery_address",
            "status",
            "delivery_date",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        request = self.context.get("request")
        if request and data.get("order"):
            if data["order"].user != request.user:
                raise serializers.ValidationError(
                    {"order": "You can only create deliveries for your own orders."}
                )
        if request and data.get("delivery_address"):
            if data["delivery_address"].user != request.user:
                raise serializers.ValidationError(
                    {"delivery_address": "You can only use your own addresses."}
                )

        return data

    def validate_delivery_date(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Delivery date cannot be in the past.")
        return value