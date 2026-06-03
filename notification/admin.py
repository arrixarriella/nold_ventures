from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'status', 'sent_at')
    list_filter = ('channel', 'status')
    search_fields = ('user__username', 'message')
    ordering = ('-sent_at',)