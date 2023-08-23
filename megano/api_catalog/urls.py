from django.urls import path
from .api_views import (
    CategoryListAPIView,
    TagListAPIView,
    ProductDetailAPIViews,
    ProductReviewCreateAPIView,
    CatalogAPIView,
    PopularProductsAPIView,
    LimitedProductAPIView, SalesAPIView, BannersAPIView
)

app_name = 'api_catalog'

urlpatterns = [
    path('api/categories/', CategoryListAPIView.as_view(), name='categories'),
    path('api/tags/', TagListAPIView.as_view()),
    path('api/product/<int:pk>/', ProductDetailAPIViews.as_view()),
    path('api/product/<int:pk>/reviews/', ProductReviewCreateAPIView.as_view()),
    path('api/catalog/', CatalogAPIView.as_view()),
    path('api/products/popular/', PopularProductsAPIView.as_view()),
    path('api/products/limited/', LimitedProductAPIView.as_view()),
    path('api/sales/', SalesAPIView.as_view()),
    path('api/banners/', BannersAPIView.as_view()),
]
