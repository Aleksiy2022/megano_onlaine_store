from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag
from .utils import set_if_not_empty
from .models import (
    Category,
    Product,
    ProductReview
)
from .pagination import MyPaginationClass
from . import serializers
from django.db.models.query import QuerySet


@extend_schema(tags=['Catalog'])
class CategoryListAPIView(ListAPIView):
    """
    Отобразить список категорий магазина.
    """

    queryset = Category.objects.filter(categories_id=None).all()
    serializer_class = serializers.CategorySerializer
    pagination_class = None


@extend_schema(tags=['Product'])
class ProductDetailAPIViews(APIView):
    """
    Отобразить детальные данные по продукту.
    """
    serializer_class = serializers.ProductDetailSerializer

    def get(self, request: Request, pk: int) -> Response:
        product = Product.objects.get(pk=pk)
        serializer = serializers.ProductDetailSerializer(product)
        return Response(serializer.data)


@extend_schema(tags=['Review'])
class ProductReviewAPIView(APIView):

    serializer_class = serializers.ProductReviewSerializer

    def get(self, request: Request, pk: int) -> Response:
        """
        Получить детали отзыва.
        """

        product_reviews = ProductReview.objects.filter(product_id=pk)
        serializer = serializers.ProductReviewSerializer(product_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request, pk: int) -> Response:
        """
        Публикация отзыва.
        """

        data = request.data
        author = data.get('author')
        email = data.get('email')
        text = data.get('text')
        rate = data.get('rate')
        date = data.get('date')
        new_review = ProductReview.objects.create(
            user=request.user,
            author=author,
            email=email,
            text=text,
            rate=rate,
            date=date,
            product_id=pk,
        )
        new_review.save()
        product = Product.objects.get(id=pk)
        product_reviews = product.reviews.all()
        count_reviews = len(product_reviews)
        product.rating = sum(review.rate for review in product_reviews)/count_reviews
        product.save()
        reviews = ProductReview.objects.filter(product_id=pk)
        serializer = serializers.ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Catalog'])
class CatalogAPIView(ListAPIView):
    """
    Отобразить список товаров отфильтрованных по переданным параметрам в запросе.
    """
    serializer_class = serializers.CatalogItemSerializer
    pagination_class = MyPaginationClass

    def get_queryset(self) -> QuerySet:

        filter_params: dict = {}
        set_if_not_empty(filter_params, 'name', self.request.query_params.get('filter[name]'))
        set_if_not_empty(filter_params, 'price__gt', self.request.query_params.get('filter[minPrice]'))
        set_if_not_empty(filter_params, 'price__lte', self.request.query_params.get('filter[maxPrice]'))

        if self.request.query_params.get('filter[freeDelivery]') == 'true':
            set_if_not_empty(filter_params, 'freeDelivery', True)

        if self.request.query_params.get('filter[available]') == 'true':
            set_if_not_empty(filter_params, 'available', True)

        set_if_not_empty(filter_params, 'category', self.request.query_params.get('category'))
        tags = [int(tag) for tag in self.request.query_params.getlist('tags[]')]

        if len(tags) != 0:
            set_if_not_empty(filter_params, 'tags__id__in', tags)

        limit = self.request.query_params.get('limit')
        sort = self.request.query_params.get('sort')
        sort_type = self.request.query_params.get('sortType')

        if sort_type == 'inc':
            if sort == 'reviews':
                products = (
                    Product.objects.
                    prefetch_related('images').
                    prefetch_related('tags').
                    annotate(num_reviews=Count('reviews')).
                    filter(**filter_params).
                    distinct().
                    order_by('-num_reviews')[:int(limit)]
                )
                return products
            else:
                sort = '-' + self.request.query_params.get('sort')
        else:
            if sort == 'reviews':
                products = (
                    Product.objects.
                    prefetch_related('images').
                    prefetch_related('tags').
                    annotate(num_reviews=Count('reviews')).
                    filter(**filter_params).
                    distinct().
                    order_by('num_reviews')[:int(limit)]
                )
                return products
            sort = self.request.query_params.get('sort')

        if len(filter_params) == 0:
            products =  (
                Product.objects.
                prefetch_related('images').
                prefetch_related('tags').
                all()
            )
            return products
        else:
            products = (
                Product.objects.
                prefetch_related('images').
                prefetch_related('tags').
                filter(**filter_params).
                distinct().
                order_by(sort)[:int(limit)]
            )
            return products


@extend_schema(tags=['Product'])
class PopularProductsAPIView(ListAPIView):
    """
    Отобразить популярные продукты.
    """

    serializer_class = serializers.CatalogItemSerializer

    def get_queryset(self) -> QuerySet:
        queryset = (
            Product.objects.
            prefetch_related('images').
            order_by('rating').
            annotate(num_reviews=Count('reviews')).
            order_by('-num_reviews')[:4]
        )
        return queryset


@extend_schema(tags=['Product'])
class LimitedProductAPIView(ListAPIView):
    """
    Отобразить список продуктов с маленьким остатком.
    """

    serializer_class = serializers.CatalogItemSerializer

    def get_queryset(self) -> QuerySet:
        return Product.objects.filter(count__lte=10).order_by('rating')[:4]


@extend_schema(tags=['Catalog'])
class SalesAPIView(ListAPIView):
    """
    Отобразить товары участвующие в акции.
    """

    queryset = (
        Product.objects.
        prefetch_related("images").
        filter(discount=True)
    )
    serializer_class = serializers.SaleSerializer
    pagination_class = MyPaginationClass


@extend_schema(tags=['Catalog'])
class BannersAPIView(ListAPIView):
    """
    Отобразить самые популярные товары с наибольшим числом отзывов и лучшим рейтингом.
    """

    queryset = (
        Product.objects.
        annotate(num_reviews=Count('reviews')).
        order_by('-num_reviews').
        order_by('-rating')[:3]
    )
    serializer_class = serializers.CatalogItemSerializer


@extend_schema(tags=['Tag'])
class TagListAPIView(ListAPIView):
    """
    Отобразить список тегов.
    """

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None
