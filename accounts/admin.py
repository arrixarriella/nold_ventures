from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    OTPVerification,
    UserAddress,
    FirebaseToken,
    NotificationPreference,
)


# =========================
# USER ADMIN
# =========================
@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        "email",
        "full_name",
        "phone_number",
        "user_type",
        "is_active",
        "is_staff",
        "created_at",
    )

    list_filter = (
        "user_type",
        "is_active",
        "is_staff",
        "is_admin",
    )

    search_fields = (
        "email",
        "full_name",
        "phone_number",
    )

    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "phone_number", "user_type")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_admin")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "full_name",
                "phone_number",
                "password1",
                "password2",
                "user_type",
                "is_staff",
                "is_active",
            ),
        }),
    )


# =========================
# OTP ADMIN
# =========================
@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "otp",
        "otp_type",
        "is_used",
        "created_at",
        "expires_at",
    )

    list_filter = (
        "otp_type",
        "is_used",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__phone_number",
        "otp",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at", "expires_at")


# =========================
# USER ADDRESS ADMIN
# =========================
@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "country",
        "province",
        "district",
        "city",
        "is_default",
        "created_at",
    )

    list_filter = (
        "country",
        "is_default",
    )

    search_fields = (
        "user__email",
        "user__phone_number",
        "province",
        "district",
        "city",
    )

    ordering = ("-created_at",)


# =========================
# FIREBASE TOKEN ADMIN
# =========================
@admin.register(FirebaseToken)
class FirebaseTokenAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "device_type",
        "created_at",
    )

    search_fields = (
        "user__email",
        "token",
    )

    ordering = ("-created_at",)


# =========================
# NOTIFICATION PREFERENCE ADMIN
# =========================
@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "push_notifications",
        "email_notifications",
        "marketing_notifications",
    )

    search_fields = (
        "user__email",
        "user__phone_number",
    )