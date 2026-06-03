from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    OrdersViewSet,
    OrderItemViewSet,
    OrdersPaymentViewSet,
    SubscriptionsViewSet,
    SubscriptionItemViewSet,
    SubscriptionPaymentViewSet,
    DeliveryViewSet
)

router = DefaultRouter()

router.register(r"deliveries", DeliveryViewSet, basename="deliveries")
router.register(r"order-items", OrderItemViewSet, basename="order-items")
router.register(r"order-payments", OrdersPaymentViewSet, basename="order-payments")
router.register(r"orders", OrdersViewSet, basename="orders")
router.register(r"subscription-items", SubscriptionItemViewSet, basename="subscription-items")
router.register(r"subscription-payments", SubscriptionPaymentViewSet, basename="subscription-payments")
router.register(r"subscriptions", SubscriptionsViewSet, basename="subscriptions")


urlpatterns = [
    path("", include(router.urls)),
]