from django.contrib import admin

from .models import (
    Category,
    CategoryImage,
    Product,
    ProductImage,
    ProductReview,
    ProductSpecifications
)


class CategoryInline(admin.StackedInline):
    model = CategoryImage

class ProductInline(admin.StackedInline):
    model = ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'title', 'categories_id',

    inlines = [
        CategoryInline,
    ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]

    list_display = (
        'title',
        'category',
        'price',
        'salePrice',
        'dateFrom',
        'dateTo',
        'discount',
        'count',
        'date',
        'available',
        'description',
        'freeDelivery',
        'tags',
        'rating',
    )


@admin.register(ProductReview)
class ProductPreviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
        'email',
        'text',
        'rate',
        'date',
        'product'
    )


@admin.register(ProductSpecifications)
class ProductSpecificationsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'value',
        'product',
    )
