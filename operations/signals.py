from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Orders, Subscriptions
from accounts.utils import send_order_notification, send_subscription_notification


@receiver(post_save, sender=Orders)
def order_created(sender, instance, created, **kwargs):
    if created:
        send_order_notification(instance)


@receiver(post_save, sender=Subscriptions)
def subscription_created(sender, instance, created, **kwargs):
    if created:
        send_subscription_notification(instance)