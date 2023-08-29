from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from api_catalog.models import Product


class Order(models.Model):
    """
    Модель заказа.
    """

    objects = models.Manager()

    user = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fullName = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = PhoneNumberField(unique=False, null=True)
    deliveryType = models.CharField(max_length=100, null=True, blank=True)
    paymentType = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True, default='unaccepted')
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    paid = models.BooleanField(default=False)
    total_order_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-createdAt']
        indexes = [
            models.Index(fields=['-createdAt']),
        ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    """
    Модель позиций в заказе.
    """

    objects = models.Manager()

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)

    def get_cost(self):
        return self.price * self.count

    def get_count(self):
        return self.count
