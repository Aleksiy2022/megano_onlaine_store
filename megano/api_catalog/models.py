from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


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
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


def category_image_directory_path(instance: "CategoryImage", filename: str) -> str:
    return "categories/category_{pk}/img/{filename}".format(
        pk=instance.category.pk,
        filename=filename
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


class Product(models.Model):
    objects = models.Manager()

    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    count = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    available = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=100)
    fullDescription = models.TextField(max_length=500, blank=True, null=True)
    freeDelivery = models.BooleanField(default=True)
    tags = TaggableManager()
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dateFrom = models.DateTimeField(blank=True, null=True)
    dateTo = models.DateTimeField(blank=True, null=True)
    discount = models.BooleanField(default=False)


    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


def product_image_directory_path(instance: "ProductImage", filename: str) -> str:
    return 'products/product_{id}/img/{filename}'.format(
        id=instance.product.pk,
        filename=filename
    )


class ProductImage(models.Model):
    objects = models.Manager()

    src = models.ImageField(upload_to=product_image_directory_path)
    alt = models.TextField(max_length=200)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )


class ProductReview(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    text = models.TextField(max_length=1000)
    rate = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')


class ProductSpecifications(models.Model):
    objects = models.Manager()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.product}'

