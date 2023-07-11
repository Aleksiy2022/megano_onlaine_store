from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CategoryListView,
    # ProductViewSet,
    # TagViewSet
)


app_name = 'api_catalog'


urlpatterns = [
    # path('', include(routers.urls)),
    path('api/categories/', CategoryListView.as_view(), name='categories')
]
