from django.urls import path
from .views import RegisterView, LoginView, GenerateOTPView, VerifyOTPView, MeView

urlpatterns = [
    path("auth/register/",     RegisterView.as_view(),    name="register"),
    path("auth/login/",        LoginView.as_view(),       name="login"),
    path("auth/otp/generate/", GenerateOTPView.as_view(), name="otp-generate"),
    path("auth/otp/verify/",   VerifyOTPView.as_view(),   name="otp-verify"),
    path("users/me/",          MeView.as_view(),          name="user-me"),
]
