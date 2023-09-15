from celery import shared_task
from django.core.mail import send_mail
from api_auth.models import Profile
from api_catalog.models import Product
from .models import Order, OrderItem


@shared_task
def create_order(request_data, order_id):

    order = Order.objects.get(pk=order_id)
    for product in request_data:
        OrderItem.objects.create(
            order=order,
            product=Product.objects.filter(id=product['id']).first(),
            price=product['price'],
            count=product['count']
        )

@shared_task
def update_order(order_id, user_id, request_data):
    total_order_cost = float(request_data['totalCost'])
    delivery_type = request_data['deliveryType']
    if delivery_type == 'express':
        total_order_cost += 500
    else:
        if total_order_cost < 2000:
            total_order_cost += 200
    Order.objects.filter(id=order_id).update(
        user_id=user_id,
        fullName=request_data['fullName'],
        email=request_data['email'],
        phone=request_data['phone'],
        deliveryType=delivery_type,
        total_order_cost=total_order_cost,
        paymentType=request_data['paymentType'],
        status=request_data['status'],
        city=request_data['city'],
        address=request_data['address'],
    )

@shared_task
def order_payment_confirmation(order_id, user_id):
    order = Order.objects.get(pk=order_id)
    profile = Profile.objects.get(user_id=user_id)
    subject = f'Megano'
    message = f'Dear {profile.user.username},\n\n' \
              f'You paid for the order number:{order_id}.\n' \
              f'Total order cost: {order.total_order_cost}$'
    mail_sent = send_mail(
        subject,
        message,
        'admin@megano.com',
        [order.email]
    )
    return mail_sent
