import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

def send_order_emails(order):
    subject = f"New Order Received — COCARRY | Order #{str(order.order_id).upper()}"
    context = {"order": order}
    html = render_to_string("emails/order_notification.html", context)
    text = render_to_string("emails/order_notification.txt", context)
    message = EmailMultiAlternatives(
        subject, text, settings.DEFAULT_FROM_EMAIL, [settings.COCARRY_BRAND_EMAIL]
    )
    message.attach_alternative(html, "text/html")
    try:
        message.send(fail_silently=False)
    except Exception:
        logger.exception("Brand order email failed for order %s", order.order_id)

    customer_subject = f"Your COCARRY order is confirmed | #{str(order.order_id).upper()}"
    customer_html = render_to_string("emails/customer_confirmation.html", context)
    customer_text = f"Thanks for shopping COCARRY. Your order #{str(order.order_id).upper()} is placed. Total: ₹{order.total_amount}."
    customer_message = EmailMultiAlternatives(
        customer_subject, customer_text, settings.DEFAULT_FROM_EMAIL, [order.customer_email]
    )
    customer_message.attach_alternative(customer_html, "text/html")
    try:
        customer_message.send(fail_silently=False)
    except Exception:
        logger.exception("Customer confirmation email failed for order %s", order.order_id)
