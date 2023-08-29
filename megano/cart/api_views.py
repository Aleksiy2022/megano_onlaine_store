from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from api_catalog.models import Product
from api_catalog.serializers import CatalogItemSerializer
from .models import Cart
from rest_framework import serializers
from typing import Type


@extend_schema(tags=['Cart'])
class CartAPIView(APIView):

    serializer_class = CatalogItemSerializer

    def get(self, request: Request) -> Response:
        """
        Получает данные по корзине.
        """

        cart = self.get_cart(request)
        serializer_data = self.get_products(cart)
        return Response(serializer_data)

    def post(self, request: Request) -> Response:
        """
        Обновить данные корзины.
        """

        cart = self.get_cart(request)
        product_id = request.data['id']
        count = request.data['count']
        cart.add_product(product_id=product_id, count=count)
        serializer_data = self.get_products(cart)
        return Response(serializer_data)

    def delete(self, request: Request) -> Response:
        """
        Удалить товар из корзины.
        """

        cart = self.get_cart(request)
        product_id = request.data['id']
        count = 0 - int(request.data['count'])
        cart.update_count_product(product_id=product_id, count=count)
        serializer_data = self.get_products(cart)
        return Response(serializer_data)

    def get_cart(self, request: Request) -> Cart:
        """
        Получить корзину из БД, при её отсутствии - создать её.
        """

        if request.session.session_key is None:
            request.session.create()
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user_id=request.user.pk)[0]
        else:
            cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]
        return cart

    def get_products(self, cart: Cart) -> Type[serializers.Serializer]:
        """
        Получить список товаров корзины.
        """

        path = self.request.path
        products = cart.items.all()
        counts_products = {str(product.product_id): str(product.count) for product in products}
        products = Product.objects.filter(id__in=counts_products.keys())
        serializer = CatalogItemSerializer(
            products,
            context={
                'counts_products': counts_products,
                'path': path
            },
            many=True
        )
        return serializer.data
