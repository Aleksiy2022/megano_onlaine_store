from api_order.models import Order

def payment_order(order_id: int, cart_number: str, month: str, year: str, code_cvv: str) -> bool:
    """
    Валидация данных для оплаты заказа.
    :param order_id: int, id заказа
    :param cart_number: str
    :param month: str
    :param year: str
    :param code_cvv: str
    :return: Возвращает True при оплате, False при не валидных данных.
    """

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
        return False
