from django.contrib import admin

from .models import Category, CategoryImage


class CategoryInline(admin.StackedInline):
    model = CategoryImage


@admin.register(Category)
class CategoryInline(admin.ModelAdmin):
    list_display = 'title', 'categories_id',

    inlines = [
        CategoryInline,
    ]
