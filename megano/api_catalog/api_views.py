from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework import status
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
from .serializers import (
    CategorySerializer,
    TagSerializer,
    ProductDetailSerializer,
    ProductReviewSerializer,
    CatalogItemSerializer, SaleSerializer,
)

class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.select_related('image').all()
    serializer_class = CategorySerializer
    pagination_class = None


class TagListAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class ProductDetailAPIViews(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class ProductReviewCreateAPIView(APIView):
    def get(self, request, pk):
        product_reviews = ProductReview.objects.filter(product_id=pk)
        serializer = ProductReviewSerializer(product_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, pk):
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
        serializer = ProductReviewSerializer(new_review)
        return Response(serializer.data)


class CatalogAPIView(ListAPIView):
    serializer_class = CatalogItemSerializer
    pagination_class = MyPaginationClass

    def get_queryset(self):
        filter_params = {}
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
                return (
                    Product.objects.
                    annotate(num_reviews=Count('reviews')).
                    filter(**filter_params).
                    order_by('-num_reviews')[:int(limit)]
                )
            else:
                sort = '-' + self.request.query_params.get('sort')
        else:
            if sort == 'reviews':
                return (
                    Product.objects.
                    annotate(num_reviews=Count('reviews')).
                    filter(**filter_params).
                    order_by('num_reviews')[:int(limit)]
                )
            sort = self.request.query_params.get('sort')

        if len(filter_params) == 0:
            return Product.objects.all()
        else:
            return Product.objects.filter(**filter_params).order_by(sort)[:int(limit)]


class PopularProductsAPIView(ListAPIView):
    serializer_class = CatalogItemSerializer

    def get_queryset(self):
        queryset = Product.objects.order_by('rating').annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
        return queryset

class LimitedProductAPIView(ListAPIView):
    serializer_class = CatalogItemSerializer

    def get_queryset(self):
        return Product.objects.filter(count__lte=10).order_by('rating')


class SalesAPIView(ListAPIView):
    queryset = Product.objects.filter(discount=True)
    serializer_class = SaleSerializer
    pagination_class = MyPaginationClass


class BannersAPIView(ListAPIView):
    queryset = Product.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews').order_by('-rating')[:3]
    serializer_class = CatalogItemSerializer
