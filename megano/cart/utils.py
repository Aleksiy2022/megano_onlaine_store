from cart.models import Cart


def merge_carts(request=None, user=None):

    session_key = request.session.session_key
    unauthorized_user_cart = Cart.objects.filter(session_key=session_key)
    user_cart = Cart.objects.filter(user=user.pk).first()

    if unauthorized_user_cart and user_cart is None:
        unauthorized_user_cart.update(user_id=user.pk)

    if unauthorized_user_cart and user_cart:
        product_counts = {str(product.product_id): str(product.count) for product in
                          unauthorized_user_cart.first().items.all()}

        for product_id, count in product_counts.items():
            user_cart.add_product(product_id, count)
