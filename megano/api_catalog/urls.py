from django.urls import path
from . import api_views

app_name = 'api_catalog'

urlpatterns = [
    path('api/categories/', api_views.CategoryListAPIView.as_view(), name='categories'),
    path('api/tags/', api_views.TagListAPIView.as_view()),
    path('api/product/<int:pk>/', api_views.ProductDetailAPIViews.as_view()),
    path('api/product/<int:pk>/reviews/', api_views.ProductReviewAPIView.as_view()),
    path('api/catalog/', api_views.CatalogAPIView.as_view()),
    path('api/products/popular/', api_views.PopularProductsAPIView.as_view()),
    path('api/products/limited/', api_views.LimitedProductAPIView.as_view()),
    path('api/sales/', api_views.SalesAPIView.as_view()),
    path('api/banners/', api_views.BannersAPIView.as_view()),
]
