from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField
from .models import (
    Category,
    CategoryImage,
    Product,
    ProductImage,
    ProductReview,
    ProductSpecifications
)
from taggit.models import Tag
from django.db.models import Avg


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = (
            'src',
            'alt',
        )


class RecursiveCategorySerializer(serializers.Serializer):
    def to_representation(self, instance):
        serialized = self.parent.parent.__class__(instance, context=self.context)
        return serialized.data


class FilterCategoryListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(categories=None)
        return super().to_representation(data)


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveCategorySerializer(many=True)
    image = CategoryImageSerializer()

    class Meta:
        list_serializer_class = FilterCategoryListSerializer
        model = Category
        fields = (
            'id',
            'title',
            'image',
            'subcategories',
        )


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
    rating = serializers.SerializerMethodField()
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

    def get_rating(self, obj):
        return ProductReview.objects.filter(product_id=obj.pk).aggregate(Avg('rate'))['rate__avg']

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
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

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

    def get_price(self, obj):
        if obj.discount:
            return obj.salePrice
        else:
            return obj.price

    def get_count(self, obj):
        counts = self.context.get('counts_products')
        path = self.context.get('path')
        if path == '/api/basket':
            return counts[str(obj.pk)]
        else:
            return obj.count

    def get_reviews(self, obj):
        return ProductReview.objects.filter(product_id=obj.pk).count()

    def get_rating(self, obj):
        return ProductReview.objects.filter(product_id=obj.pk).aggregate(Avg('rate'))['rate__avg']


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
