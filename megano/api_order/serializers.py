from django.db.models import Avg
from rest_framework import serializers

from api_catalog.models import ProductReview
from api_catalog.serializers import ProductImageSerializer, TagSerializer
from api_order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='product.id')
    category = serializers.CharField(source='product.category')
    price = serializers.SerializerMethodField()
    count = serializers.CharField(source='get_count')
    date = serializers.DateTimeField(source='product.date')
    title = serializers.CharField(source='product.title')
    description = serializers.CharField(source='product.description')
    freeDelivery = serializers.CharField(source='product.freeDelivery')
    images = ProductImageSerializer(source='product.images', many=True)
    tags = TagSerializer(source='product.tags', many=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'rating',
        )

    def get_price(self, obj):
        if obj.product.discount:
            return obj.product.salePrice
        else:
            return obj.product.price

    def get_reviews(self, obj):
        return ProductReview.objects.filter(product_id=obj.product.pk).count()

    def get_rating(self, obj):
        return ProductReview.objects.filter(product_id=obj.product.pk).aggregate(Avg('rate'))['rate__avg']

class OrderSerializer(serializers.ModelSerializer):

    createdAt = serializers.DateTimeField()
    email = serializers.EmailField()
    totalCost = serializers.SerializerMethodField()
    products = OrderItemSerializer(source='items', many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
            'products',
        )

    def get_totalCost(self, order):
        if order.paid:
            return order.total_order_cost
        else:
            return order.total_cost()
