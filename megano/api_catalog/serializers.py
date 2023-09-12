from rest_framework import serializers
from taggit.serializers import TaggitSerializer
from .models import (
    Category,
    CategoryImage,
    Product,
    ProductImage,
    ProductReview,
    ProductSpecifications
)
from taggit.models import Tag
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer, OpenApiExample


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = (
            'src',
            'alt',
        )


@extend_schema_serializer(
    examples=[
         OpenApiExample(
            'Category',
            value={
                'id': 1,
                'title': 'Компьютеры',
                'image': {
                    'src': '/3.png',
                    'alt': 'Image alt string'
                 },
                'subcategories': {
                    'id': 8,
                    'title': 'Мониторы',
                    'image': {
                        'src': '/3.png',
                        'alt': 'Image alt string'
                    },
                    }
            },
        ),
    ]
)
class CategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer()

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'image',
            'subcategories',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        subcategories_data = self.__class__(instance.subcategories.all(), many=True).data
        data['subcategories'] = subcategories_data
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name'
        )


class ProductSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecifications
        fields = (
            'name',
            'value',
        )


class ProductReviewSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    rate = serializers.IntegerField(min_value=0, max_value=5)
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = ProductReview
        fields = (
            'author',
            'email',
            'text',
            'rate',
            'date',
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'src',
            'alt',
        )


class ProductDetailSerializer(TaggitSerializer, serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    images = ProductImageSerializer(many=True)
    reviews = ProductReviewSerializer(many=True)
    specifications = ProductSpecificationsSerializer(many=True)
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'fullDescription',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'specifications',
            'rating',
        )

    @extend_schema_field(OpenApiTypes.STR)
    def get_price(self, obj):
        if obj.discount:
            return obj.salePrice
        else:
            return obj.price


class CatalogItemSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    freeDelivery = serializers.BooleanField()
    images = ProductImageSerializer(many=True)
    tags = serializers.SerializerMethodField()
    reviews = serializers.CharField(source='reviews_count')

    class Meta:
        model = Product
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
        if obj.discount:
            return obj.salePrice
        else:
            return obj.price

    @extend_schema_field(OpenApiTypes.STR)
    def get_count(self, obj):
        counts = self.context.get('counts_products')
        path = self.context.get('path')
        if path == '/api/basket':
            return counts[str(obj.pk)]
        else:
            return obj.count

    @extend_schema_field(OpenApiTypes.STR)
    def get_tags(self, obj):
        path = self.context.get('path')
        if path == '/api/basket':
            return None
        tags = obj.tags.all()
        serializer = TagSerializer(tags, many=True)
        return serializer.data


class SaleSerializer(serializers.ModelSerializer):

    dateFrom = serializers.DateTimeField(format='%m-%d')
    dateTo = serializers.DateTimeField(format='%m-%d')
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'price',
            'salePrice',
            'dateFrom',
            'dateTo',
            'title',
            'images',
        )
