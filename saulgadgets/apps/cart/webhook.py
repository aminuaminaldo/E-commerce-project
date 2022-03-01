import json
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string 

from .cart import Cart

from apps.order.models import Order

@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN 
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object

        order = Order.objects.get(payment_intent=payment_intent.id)
        order.paid = True
        order.save()

        for item in Order.items.all():
            product = item.product
            product.num_available = product.num_available - item.quantity
            product.save()
        
        html = render_to_string('email_confirmation.html', {'order': order})
        send_mail('Order Confirmation', 'Your order has successful', 'noreply@saulgadgets.com', ['mail@aminu.com', order.email], fail_silently=True, html_message=html)
    return HttpResponse(status=200)
