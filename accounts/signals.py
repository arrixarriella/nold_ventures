from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# ─────────────────────────────────────────────
# CREATE NOTIFICATION PREFERENCES ON USER CREATION
# ─────────────────────────────────────────────

@receiver(post_save, sender=User)
def create_notification_preference(sender, instance, created, **kwargs):
    if created:
        from .models import NotificationPreference
        NotificationPreference.objects.get_or_create(user=instance)


# ─────────────────────────────────────────────
# ENFORCE SINGLE DEFAULT ADDRESS
# ─────────────────────────────────────────────

@receiver(post_save, sender="accounts.UserAddress")  # 👈 was "users.UserAddress"
def enforce_single_default_address(sender, instance, **kwargs):
    if instance.is_default:
        from .models import UserAddress
        UserAddress.objects.filter(
            user=instance.user,
            is_default=True,
        ).exclude(pk=instance.pk).update(is_default=False)


# ─────────────────────────────────────────────
# AUTO-SET DEFAULT ADDRESS IF NONE EXISTS
# ─────────────────────────────────────────────

@receiver(post_save, sender="accounts.UserAddress")  # 👈 was "users.UserAddress"
def auto_set_default_address(sender, instance, created, **kwargs):
    if created:
        from .models import UserAddress
        is_only_address = (
            UserAddress.objects.filter(user=instance.user).count() == 1
        )
        if is_only_address and not instance.is_default:
            UserAddress.objects.filter(pk=instance.pk).update(is_default=True)


# ─────────────────────────────────────────────
# CLEAN UP FIREBASE TOKENS ON USER DELETION
# ─────────────────────────────────────────────

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    from .models import FirebaseToken
    FirebaseToken.objects.filter(user=instance).delete()


# ─────────────────────────────────────────────
# MARK USER AS NO LONGER FIRST LOGIN
# ─────────────────────────────────────────────

@receiver(post_save, sender=User)
def clear_first_login_flag(sender, instance, created, **kwargs):
    if not created and instance.is_first_login:
        User.objects.filter(pk=instance.pk).update(is_first_login=False)