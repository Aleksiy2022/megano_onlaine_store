from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_catalog.models import Product
from api_catalog.serializers import CatalogItemSerializer
from .models import Cart


class CartAPIView(APIView):
    def get(self, request):
        cart = self.get_cart(request)
        serializer_data = self.get_products(cart)
        return Response(serializer_data)

    def post(self, request):
        cart = self.get_cart(request)
        product_id = request.data['id']
        count = request.data['count']
        cart.add_product(product_id=product_id, count=count)
        serializer_data = self.get_products(cart)
        return Response(serializer_data)

    def delete(self, request):
        cart = self.get_cart(request)
        product_id = request.data['id']
        count = 0 - int(request.data['count'])
        cart.update_count_product(product_id=product_id, count=count)
        serializer_data = self.get_products(cart)
        return Response(serializer_data)

    def get_cart(self, request):
        if request.session.session_key is None:
            request.session.create()
            print('Ключ сессии из функции get_cart',request.session.session_key)
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user_id=request.user.pk)[0]
        else:
            print('сработал блок else')
            print('Ключ сессии из функции get_cart', request.session.session_key)
            cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]
        return cart

    def get_products(self, cart):
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