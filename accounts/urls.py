from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    GenerateOTPView,
    VerifyOTPView,
    MeView,
    AddressFieldsView,
    UserAddressViewSet,
    NotificationPreferenceView,
    FirebaseTokenView,
)

router = DefaultRouter()
router.register(r"addresses", UserAddressViewSet, basename="user-address")

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────
    path("auth/register/",      RegisterView.as_view(),    name="register"),
    path("auth/otp/generate/",  GenerateOTPView.as_view(), name="otp-generate"),
    path("auth/otp/verify/",    VerifyOTPView.as_view(),   name="otp-verify"),

    # ── User ──────────────────────────────────────────────
    path("users/me/",           MeView.as_view(),          name="user-me"),

    # ── Addresses ─────────────────────────────────────────
    path("users/addresses/fields/", AddressFieldsView.as_view(), name="address-fields"),
    path("users/",                  include(router.urls)),

    # ── Notifications ─────────────────────────────────────
    path("users/notifications/preferences/", NotificationPreferenceView.as_view(), name="notification-preferences"),

    # ── Firebase ──────────────────────────────────────────
    path("users/firebase-token/", FirebaseTokenView.as_view(), name="firebase-token"),
]