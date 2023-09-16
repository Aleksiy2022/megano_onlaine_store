from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


class Category(models.Model):
    """
    Модель Категории товаров.
    """

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
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


def category_image_directory_path(instance: "CategoryImage", filename: str) -> str:
    """
    :param instance: CategoryImage
    :param filename: str
    :return: str, путь для получения изображения категории
    """

    return "categories/category_{pk}/img/{filename}".format(
        pk=instance.category.pk,
        filename=filename
    )


class CategoryImage(models.Model):
    """
    Модель для хранения изображения категории.
    """

    objects = models.Manager()

    src = models.ImageField(upload_to=category_image_directory_path)
    alt = models.CharField(max_length=200)
    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='image',
    )

    class Meta:
        verbose_name = 'Изображение категории'
        verbose_name_plural = 'Изображения категори'


class Product(models.Model):
    """
    Модель товара.
    """

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
    reviews_count = models.PositiveIntegerField(default=0)
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dateFrom = models.DateTimeField(blank=True, null=True)
    dateTo = models.DateTimeField(blank=True, null=True)
    discount = models.BooleanField(default=False)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    class Meta:
        ordering = ['id']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.discount:
            self.current_price = self.salePrice
        else:
            self.current_price = self.price
        super().save(*args, **kwargs)


def product_image_directory_path(instance: "ProductImage", filename: str) -> str:
    """
    :param instance: ProductImage
    :param filename: str
    :return: str, путь для получения изображений товаров
    """

    return 'products/product_{id}/img/{filename}'.format(
        id=instance.product.pk,
        filename=filename
    )


class ProductImage(models.Model):
    """
    Модель для хранения изображения товаров.
    """

    objects = models.Manager()

    src = models.ImageField(upload_to=product_image_directory_path)
    alt = models.TextField(max_length=200)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изоюражения товара'


class ProductReview(models.Model):
    """
    Модель отзыва.
    """

    objects = models.Manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    text = models.TextField(max_length=1000)
    rate = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = 'Отзыв на товар'
        verbose_name_plural = 'Отзывы на товары'


class ProductSpecifications(models.Model):
    """
    Модель характеристик товара.
    """

    objects = models.Manager()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'Характеристики продукта'
        verbose_name_plural = 'Характеристики продуктов'

