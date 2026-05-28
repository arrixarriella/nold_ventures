import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OTPVerification, UserAddress, FirebaseToken, NotificationPreference
from .permissions import IsOwner, IsActiveUser
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    OTPVerificationSerializer,
    UserAddressSerializer,
    FirebaseTokenSerializer,
    NotificationPreferenceSerializer,
)
from .utils import generate_and_send_otp

User = get_user_model()

# USER REGISTRATION

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully.",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GENERATE OTP

class GenerateOTPView(APIView):
    """
    POST /api/v1/auth/otp/generate/
    Body: { "user_id": 1, "otp_type": "email" | "sms" | "both" }
    Generates a 6-digit OTP and sends it via email and/or SMS.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        user_id  = request.data.get("user_id")
        otp_type = request.data.get("otp_type")

        if not user_id:
            return Response(
                {"error": "user_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        generate_and_send_otp(user, otp_type=otp_type)

        return Response(
            {"message": "OTP sent to your email and phone number."},
            status=status.HTTP_200_OK,
        )

# VERIFY OTP

class VerifyOTPView(APIView):
    """
    POST /api/v1/auth/otp/verify/
    Body: { "user_id": 1, "otp": "123456" }
    Verifies the OTP and activates the user if not already active.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        user_id  = request.data.get("user_id")
        otp_code = request.data.get("otp")

        if not user_id or not otp_code:
            return Response(
                {"error": "user_id and otp are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            otp = OTPVerification.objects.filter(
                user_id=user_id,
                otp=otp_code,
                is_used=False,
            ).latest("created_at")

        except OTPVerification.DoesNotExist:
            return Response(
                {"error": "Invalid OTP. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp.is_expired():
            return Response(
                {"error": "OTP has expired. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp.is_used = True
        otp.save()

        user = otp.user
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

        return Response(
            {"message": "OTP verified successfully."},
            status=status.HTTP_200_OK,
        )

# CURRENT USER PROFILE

class MeView(generics.RetrieveUpdateAPIView):
    """
    GET    /api/v1/users/me/  → return logged-in user's profile
    PATCH  /api/v1/users/me/  → update logged-in user's profile
    """
    serializer_class   = UserSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]

    def get_object(self):
        return self.request.user

# ADDRESS FIELDS — DYNAMIC FORM HELPER


class AddressFieldsView(APIView):
    """
    GET /api/v1/users/addresses/fields/?country=RW
    Returns which fields are required / hidden for the given country.
    The frontend uses this to show or hide form fields dynamically.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        country = request.query_params.get("country", "").strip().upper()

        if not country:
            return Response(
                {"error": "country query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if country == "RW":
            return Response({
                "country":         "RW",
                "address_type":    "rwanda",
                "required_fields": ["province", "district", "sector", "cell", "village"],
                "hidden_fields":   ["city", "street_number", "house_number"],
                "labels": {
                    "province": "Province",
                    "district": "District",
                    "sector":   "Sector",
                    "cell":     "Cell",
                    "village":  "Village",
                },
            })

        return Response({
            "country":         country,
            "address_type":    "international",
            "required_fields": ["city", "street_number", "house_number"],
            "hidden_fields":   ["province", "district", "sector", "cell", "village"],
            "labels": {
                "city":          "City",
                "street_number": "Street Number",
                "house_number":  "House Number",
            },
        })



# USER ADDRESS


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    GET    /api/v1/users/addresses/          → list all addresses for logged-in user
    POST   /api/v1/users/addresses/          → create a new address
    GET    /api/v1/users/addresses/<id>/     → retrieve a single address
    PUT    /api/v1/users/addresses/<id>/     → full update
    PATCH  /api/v1/users/addresses/<id>/     → partial update
    DELETE /api/v1/users/addresses/<id>/     → delete
    """
    serializer_class   = UserAddressSerializer
    permission_classes = [IsAuthenticated, IsActiveUser, IsOwner]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

# NOTIFICATION PREFERENCES


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    """
    GET        /api/v1/users/notifications/preferences/  → get preferences
    PUT/PATCH  /api/v1/users/notifications/preferences/  → update preferences
    Auto-creates default preferences if none exist yet.
    """
    serializer_class   = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]

    def get_object(self):
        obj, _ = NotificationPreference.objects.get_or_create(user=self.request.user)
        return obj

# FIREBASE TOKEN


class FirebaseTokenView(APIView):
    """
    POST   /api/v1/users/firebase-token/  → register or update a device FCM token
    DELETE /api/v1/users/firebase-token/  → remove a device FCM token on logout
    """
    permission_classes = [IsAuthenticated, IsActiveUser]

    def post(self, request):
        serializer = FirebaseTokenSerializer(
            data=request.data,
            context={"request": request},
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token       = request.data.get("token")
        device_type = request.data.get("device_type")

        if not token or not device_type:
            return Response(
                {"error": "token and device_type are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    
        FirebaseToken.objects.update_or_create(
            user=request.user,
            device_type=device_type,
            defaults={"token": token},
        )

        return Response(
            {"message": "Firebase token saved successfully."},
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_count, _ = FirebaseToken.objects.filter(
            user=request.user,
            token=token,
        ).delete()

        if deleted_count:
            return Response(
                {"message": "Token removed successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Token not found."},
            status=status.HTTP_404_NOT_FOUND,
        )