from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django_countries.fields import CountryField



# USER MANAGER

class UserManager(BaseUserManager):

    def create_user(self, email, full_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password=None, **extra_fields):
        user = self.create_user(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            password=password,
            **extra_fields,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


# =========================
# USER MODEL
# =========================
class User(AbstractUser, PermissionsMixin):

    CLIENT = "CLIENT"
    FARMER = "FARMER"
    ADMIN = "ADMIN"

    USER_TYPE_CHOICES = [
        (CLIENT, "Client"),
        (FARMER, "Farmer"),
        (ADMIN, "Admin"),
    ]

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(max_length=255)

    phone_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[MinLengthValidator(10), MaxLengthValidator(13)]
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default=CLIENT
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    is_first_login = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "phone_number"]

    objects = UserManager()

    def __str__(self):
        return self.email



# OTP VERIFICATION (EMAIL + SMS)

class OTPVerification(models.Model):

    EMAIL = "email"
    SMS = "sms"
    BOTH = "both"

    OTP_TYPE_CHOICES = [
        (EMAIL, "Email"),
        (SMS, "SMS"),
        (BOTH, "Email & SMS"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otp_codes")
    otp = models.CharField(max_length=6)

    otp_type = models.CharField(max_length=10, choices=OTP_TYPE_CHOICES, default=BOTH)

    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.email} - {self.otp}"



# USER ADDRESS 

class UserAddress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    country = CountryField()

    # Rwanda fields
    province = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    cell = models.CharField(max_length=100, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)

    # International fields
    city = models.CharField(max_length=100, blank=True, null=True)
    house_number = models.CharField(max_length=50, blank=True, null=True)
    street_number = models.CharField(max_length=50, blank=True, null=True)

    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):

        country_code = str(self.country).upper()

        if country_code == "RW":
            if not all([self.province, self.district, self.sector, self.cell, self.village]):
                raise ValidationError(
                    "Rwanda address requires province, district, sector, cell and village."
                )

        else:
            if not all([self.city, self.street_number, self.house_number]):
                raise ValidationError(
                    "International address requires city, street number and house number."
                )

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.is_default:
            UserAddress.objects.filter(user=self.user).update(is_default=False)

        super().save(*args, **kwargs)


# FIREBASE TOKEN

class FirebaseToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="firebase_tokens")
    device_type = models.CharField(max_length=50)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]



# NOTIFICATION PREFERENCES

class NotificationPreference(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="notification_settings")

    push_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    marketing_notifications = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notifications - {self.user.email}"