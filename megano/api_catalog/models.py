from django.db import models
# from taggit.managers import TaggableManager


class Category(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=100)
    categories = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategories',
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


def category_image_directory_path(instance: "CategoryImage", filename: str) -> str:
    return "categories/category_{pk}/img/{filename}".format(
        pk=instance.category.pk,
        filename=filename,
    )


class CategoryImage(models.Model):
    objects = models.Manager()

    src = models.ImageField(upload_to=category_image_directory_path)
    alt = models.CharField(max_length=200)
    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='image',
    )


# class Product(models.Model):
#     objects = models.Manager()
#
#     category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     count = models.PositiveIntegerField(blank=True, null=True)
#     available = models.BooleanField()
#     date = models.DateTimeField()
#     title = models.TextField(max_length=100)
#     description = models.TextField(blank=True, max_length=500)
#     freeDelivery = models.BooleanField()
#     tag = TaggableManager()
#
#     # создать модель Review для 2-х новых полей
#     # reviews = models.ForeignKey(Review, on_delete=models.CASCADE)
#     # rating = models.DecimalField()
#
#     def __str__(self):
#         return self.title
#
#
# def product_image_directory_path(instance: "Product", filename: str) -> str:
#     return f"products/product_{id}/img/{filename}"
#
#
# class ProductImage(models.Model):
#     objects = models.Manager()
#
#     src = models.ImageField(upload_to=product_image_directory_path())
#     alt = models.TextField(max_length=200)
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name="images"
#     )
