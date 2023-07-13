from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import (
    Category,
    # Product,
    # Tag
)
from .serializers import (
    CategorySerializer,
    # ProductSerializers,
    # TagSerializers,
)


class CategoryListView(ListAPIView):
    queryset = Category.objects.select_related('image').all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.select_related("tags").all()
#     serializer_class = ProductSerializers
#
#
# class TagViewSet(ModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializers
