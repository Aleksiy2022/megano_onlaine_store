from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = \
        'id', 'user', 'createdAt', 'updated', 'email', 'phone', 'deliveryType', 'paymentType',\
        'status', 'address', 'total_order_cost', 'paid',

    inlines = [
        OrderItemInline
        ]
    ordering = 'user',
    list_filter = 'deliveryType', 'paymentType', 'status', 'paid', 'createdAt',
    search_fields = 'user__username', 'id',