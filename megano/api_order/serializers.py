from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
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
    reviews = serializers.CharField(source='product.reviews_count')
    rating = serializers.CharField(source='product.rating')

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

    @extend_schema_field(OpenApiTypes.STR)
    def get_price(self, obj):
        if obj.product.discount:
            return obj.product.salePrice
        else:
            return obj.product.price


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

    @extend_schema_field(OpenApiTypes.STR)
    def get_totalCost(self, order):
        if order.paid:
            return order.total_order_cost
        else:
            return order.total_cost()
