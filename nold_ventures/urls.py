from django.contrib import admin
from django.urls import path, include
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenRefreshView


class TaggedTokenRefreshView(TokenRefreshView):
    @extend_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TaggedSpectacularAPIView(SpectacularAPIView):
    @extend_schema(tags=["Schema"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TaggedSpectacularRedocView(SpectacularRedocView):
    @extend_schema(tags=["Schema"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


urlpatterns = [
    path("admin/",             admin.site.urls),

    # Apps
    path("api/v1/",            include("accounts.urls")),
    path("api/inventory/",     include("inventory.urls")),
    path("api/notifications/", include("notification.urls")),
    path("api/operations/",    include("operations.urls")),

    # JWT token refresh
    path("api/token/refresh/", TaggedTokenRefreshView.as_view(), name="token_refresh"),

    # Schema & Docs
    path("api/schema/",        TaggedSpectacularAPIView.as_view(), name="schema"),
    path("api/redoc/",         TaggedSpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("",                   SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
