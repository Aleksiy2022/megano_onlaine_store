from rest_framework import serializers
from .models import (
    Category,
    CategoryImage,
    # Product,
    # Tag,
)


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


# class ProductSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = (
#             "id",
#             "category",
#             "price",
#             "date",
#             "title",
#             "description",
#             "freeDelivery",
#             "images",
#             "tags",
#         )
#
#
# class TagSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = (
#             "id",
#             "name",
#         )
