import secrets
from datetime import timedelta

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags


def generate_otp(user, otp_type=None):
    from .models import OTPVerification

    if otp_type is None:
        otp_type = OTPVerification.BOTH

    OTPVerification.objects.filter(user=user, is_used=False).update(is_used=True)

    otp_code = str(secrets.randbelow(900000) + 100000)

    OTPVerification.objects.create(
        user=user,
        otp=otp_code,
        otp_type=otp_type,
        expires_at=timezone.now() + timedelta(minutes=10),
    )

    return otp_code


def send_otp_email(user, otp_code):
    subject = "Your Nold Ventures Verification Code"

    html_content = render_to_string(
        "emails/otp_email.html",
        {
            "otp_code": otp_code,
            "user": user,
            "valid_minutes": 10,
            "app_name": "Nold Ventures",
        },
    )
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email="Nold Ventures <arrimwungeri@gmail.com>",
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send OTP email to {user.email}: {e}")
        raise


def send_otp_sms(user, otp_code):
    # SMS integration can be added here later (e.g. Twilio, Africa's Talking)
    pass


def generate_and_send_otp(user, otp_type=None):
    from .models import OTPVerification

    if otp_type is None:
        otp_type = OTPVerification.BOTH

    otp_code = generate_otp(user, otp_type=otp_type)

    if otp_type in (OTPVerification.EMAIL, OTPVerification.BOTH):
        send_otp_email(user, otp_code)

    if otp_type in (OTPVerification.SMS, OTPVerification.BOTH):
        send_otp_sms(user, otp_code)

    return otp_code


# ─────────────────────────────────────────────
# ORDER NOTIFICATION
# ─────────────────────────────────────────────

def send_order_notification(order):
    user = order.user

    # ── Email ──
    try:
        html_content = render_to_string(
            "emails/order_confirmation.html",
            {
                "user": user,
                "order": order,
                "app_name": "Nold Ventures",
            },
        )
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=f"Order Confirmation – Order #{order.id}",
            body=text_content,
            from_email="Nold Ventures <arrimwungeri@gmail.com>",
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(f"[EMAIL] Order confirmation sent to {user.email}")

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send order email: {e}")

    # ── SMS ──
    try:
        send_sms(
            phone_number=user.phone_number,
            message=(
                f"Hi {user.full_name}, your order #{order.id} has been placed successfully "
                f"on {order.order_date.strftime('%d %b %Y')}. "
                f"Expected delivery: {order.delivery_date}. Thank you for choosing Nold Ventures!"
            ),
        )
    except Exception as e:
        print(f"[SMS ERROR] Failed to send order SMS: {e}")


# ─────────────────────────────────────────────
# SUBSCRIPTION NOTIFICATION
# ─────────────────────────────────────────────

def send_subscription_notification(subscription):
    user = subscription.user

    # ── Email ──
    try:
        html_content = render_to_string(
            "emails/subscription_confirmation.html",
            {
                "user": user,
                "subscription": subscription,
                "app_name": "Nold Ventures",
            },
        )
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=f"Subscription Confirmed – {subscription.frequency.capitalize()} Plan",
            body=text_content,
            from_email="Nold Ventures <arrimwungeri@gmail.com>",
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(f"[EMAIL] Subscription confirmation sent to {user.email}")

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send subscription email: {e}")

    # ── SMS ──
    try:
        send_sms(
            phone_number=user.phone_number,
            message=(
                f"Hi {user.full_name}, your {subscription.frequency} subscription #{subscription.id} "
                f"is now active starting {subscription.start_date}. "
                f"Thank you for choosing Nold Ventures!"
            ),
        )
    except Exception as e:
        print(f"[SMS ERROR] Failed to send subscription SMS: {e}")


# ─────────────────────────────────────────────
# SMS SENDER (Africa's Talking — plug in later)
# ─────────────────────────────────────────────

def send_sms(phone_number, message):
    # TODO: Integrate Africa's Talking or Twilio here
    # Example with Africa's Talking:
    # import africastalking
    # africastalking.initialize(username, api_key)
    # sms = africastalking.SMS
    # sms.send(message, [phone_number])
    print(f"[SMS] To: {phone_number} | Message: {message}")
    pass