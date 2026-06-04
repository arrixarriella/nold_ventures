from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = ["id", "email", "full_name", "phone_number", "user_type", "is_active", "created_at"]
        read_only_fields = ["id", "is_active", "created_at"]


class RegisterSerializer(serializers.ModelSerializer):

    password         = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    user_type        = serializers.ChoiceField(choices=["CLIENT", "FARMER"])

    class Meta:
        model  = User
        fields = ["email", "full_name", "phone_number", "password", "confirm_password", "user_type"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        return User.objects.create_user(**validated_data, password=password)


class LoginSerializer(serializers.Serializer):

    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            request=self.context.get("request"),
            email=data["email"],
            password=data["password"],
        )
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        data["user"] = user
        return data