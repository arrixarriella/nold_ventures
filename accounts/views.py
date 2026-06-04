from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers as rf_serializers
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPVerification
from .permissions import IsActiveUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .utils import generate_and_send_otp

User = get_user_model()


@extend_schema(tags=["Auth"], request=RegisterSerializer, responses={201: UserSerializer})
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # require OTP verification before login
            user.save(update_fields=["is_active"])
            generate_and_send_otp(user, otp_type="both")
            return Response(
                {
                    "message": "Registration successful. Check your email and phone for your OTP.",
                    "user_id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Auth"],
    request=inline_serializer(
        name="LoginRequest",
        fields={
            "email": rf_serializers.EmailField(),
            "password": rf_serializers.CharField(),
        },
    ),
    responses={200: inline_serializer(
        name="LoginResponse",
        fields={
            "access": rf_serializers.CharField(),
            "refresh": rf_serializers.CharField(),
            "user_type": rf_serializers.CharField(),
            "user": rf_serializers.DictField(),
        },
    )},
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_type": user.user_type,
            "user": UserSerializer(user).data,
        })


@extend_schema(
    tags=["Auth"],
    request=inline_serializer(
        name="GenerateOTPRequest",
        fields={
            "user_id": rf_serializers.IntegerField(),
            "otp_type": rf_serializers.ChoiceField(choices=["email", "sms", "both"]),
        },
    ),
    responses={200: inline_serializer(
        name="GenerateOTPResponse",
        fields={"message": rf_serializers.CharField()},
    )},
)
class GenerateOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id  = request.data.get("user_id")
        otp_type = request.data.get("otp_type", "both")

        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        generate_and_send_otp(user, otp_type=otp_type)
        return Response({"message": "OTP sent to your email and phone number."}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Auth"],
    request=inline_serializer(
        name="VerifyOTPRequest",
        fields={
            "user_id": rf_serializers.IntegerField(),
            "otp": rf_serializers.CharField(),
        },
    ),
    responses={200: inline_serializer(
        name="VerifyOTPResponse",
        fields={"message": rf_serializers.CharField()},
    )},
)
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id  = request.data.get("user_id")
        otp_code = request.data.get("otp")

        if not user_id or not otp_code:
            return Response({"error": "user_id and otp are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp = OTPVerification.objects.filter(
                user_id=user_id, otp=otp_code, is_used=False,
            ).latest("created_at")
        except OTPVerification.DoesNotExist:
            return Response({"error": "Invalid OTP. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            return Response({"error": "OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_used = True
        otp.save()

        user = otp.user
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

        return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(tags=["Admin Dashboard", "Client Dashboard", "Farmer Dashboard"]),
    patch=extend_schema(tags=["Admin Dashboard", "Client Dashboard", "Farmer Dashboard"]),
)
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class   = UserSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]
    http_method_names  = ["get", "patch", "head", "options"]

    def get_object(self):
        return self.request.user