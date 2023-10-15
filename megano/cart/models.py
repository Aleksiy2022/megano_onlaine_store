from django.contrib.auth.models import User
from django.db import models
from api_catalog.models import Product


class Cart(models.Model):
    """
    Модель корзины.
    """

    objects = models.Manager()

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=50, blank=True, null=True)

    def add_product(self, product_id, count):
        cart_item = self.items.filter(product=product_id).first()
        if not cart_item:
            cart_item = CartItem(cart=self, product_id=product_id, count=count)
            cart_item.save()
        else:
            self.update_count_product(cart_item=cart_item, count=count, product_id=product_id)

    def update_count_product(self, cart_item=None, count=None, product_id=None):
        if not cart_item:
            cart_item = self.items.filter(product=product_id).first()
        if count > 0:
            cart_item.count += count
            cart_item.save()
        if count < 0:
            cart_item.count += count
            cart_item.save()
            if cart_item.count <= 0:
                cart_item.delete()


class CartItem(models.Model):
    """
    Модель позиции в корзине.
    """

    objects = models.Manager()

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


