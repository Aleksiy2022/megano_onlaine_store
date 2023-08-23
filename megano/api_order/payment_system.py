from api_order.models import Order

def payment_order(order_id, cart_number, month, year, code_cvv):
    order = Order.objects.get(id=order_id)
    if order:
        if len(cart_number) == 16 and 1 <= int(month) <= 12 and 23 <= int(year) <= 99 and len(code_cvv) == 3:
            order.paid = True
            order.status = 'accepted'
            order.save()
            return order.paid
        else:
            return order.paid
    else:
        return None
