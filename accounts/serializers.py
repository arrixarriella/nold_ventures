from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_countries.fields import Country
from .models import (
    OTPVerification,
    UserAddress,
    FirebaseToken,
    NotificationPreference,
)

User = get_user_model()


# ─────────────────────────────────────────────
# USER SERIALIZER
# ─────────────────────────────────────────────

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = [
            "id",
            "email",
            "full_name",
            "phone_number",
            "user_type",
            "is_active",
            "is_first_login",
            "created_at",
        ]
        read_only_fields = ["id", "is_active", "is_first_login", "created_at"]


# ─────────────────────────────────────────────
# REGISTER SERIALIZER
# ─────────────────────────────────────────────

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": "Password must be at least 8 characters long.",
        },
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = [
            "email",
            "full_name",
            "phone_number",
            "password",
            "confirm_password",
            "user_type",
        ]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value.lower()

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists."
            )
        return value

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data, password=password)
        return user


# ─────────────────────────────────────────────
# OTP SERIALIZER
# ─────────────────────────────────────────────

class OTPVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model  = OTPVerification
        fields = [
            "id",
            "user",
            "otp",
            "otp_type",
            "is_used",
            "created_at",
            "expires_at",
        ]
        read_only_fields = ["id", "is_used", "created_at", "expires_at"]


# ─────────────────────────────────────────────
# USER ADDRESS SERIALIZER
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# USER ADDRESS SERIALIZER
# ─────────────────────────────────────────────

class UserAddressSerializer(serializers.ModelSerializer):

    # Write-only: silently sets user from request.user on create/update
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Read-only: displays full_name instead of email or raw ID
    user_full_name = serializers.CharField(
        source="user.full_name",
        read_only=True,
    )

    class Meta:
        model  = UserAddress
        fields = [
            "id",
            "user",
            "user_full_name",
            "country",
            "province",
            "district",
            "sector",
            "cell",
            "village",
            "city",
            "street_number",
            "house_number",
            "is_default",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def _get_country_code(self, value):
        if isinstance(value, Country):
            return value.code.upper()
        return str(value).strip().upper()

    def validate(self, data):
        country_code = self._get_country_code(data.get("country", ""))

        if not country_code:
            raise serializers.ValidationError(
                {"country": "Country is required."}
            )

        if country_code == "RW":
            required = ["province", "district", "sector", "cell", "village"]
            missing  = [f for f in required if not data.get(f)]

            if missing:
                raise serializers.ValidationError({
                    f: "This field is required for Rwanda addresses."
                    for f in missing
                })

            data["city"]          = None
            data["street_number"] = None
            data["house_number"]  = None

        else:
            required = ["city", "street_number", "house_number"]
            missing  = [f for f in required if not data.get(f)]

            if missing:
                raise serializers.ValidationError({
                    f: "This field is required for international addresses."
                    for f in missing
                })

            data["province"] = None
            data["district"] = None
            data["sector"]   = None
            data["cell"]     = None
            data["village"]  = None

        return data

# ─────────────────────────────────────────────
# FIREBASE TOKEN SERIALIZER
# ─────────────────────────────────────────────

class FirebaseTokenSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model  = FirebaseToken
        fields = [
            "id",
            "user",
            "device_type",
            "token",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_token(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("A valid token is required.")
        return value.strip()

    def validate_device_type(self, value):
        allowed = ["android", "ios", "web"]
        if value.lower() not in allowed:
            raise serializers.ValidationError(
                f"device_type must be one of: {', '.join(allowed)}."
            )
        return value.lower()


# ─────────────────────────────────────────────
# NOTIFICATION PREFERENCE SERIALIZER
# ─────────────────────────────────────────────

class NotificationPreferenceSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model  = NotificationPreference
        fields = [
            "id",
            "user",
            "push_notifications",
            "email_notifications",
            "marketing_notifications",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]