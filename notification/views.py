from accounts.permissions import IsActiveUser
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer


@extend_schema_view(
    get=extend_schema(tags=["Admin Dashboard", "Client Dashboard", "Farmer Dashboard"]),
)
class NotificationListView(generics.ListAPIView):
    serializer_class   = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


@extend_schema_view(
    get=extend_schema(tags=["Client Dashboard"]),
    patch=extend_schema(tags=["Client Dashboard"]),
)
class NotificationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class   = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]
    http_method_names  = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
