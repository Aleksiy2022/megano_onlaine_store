from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from api_auth.serializers import EmptySerializer
from api_catalog.models import Product
from api_order.models import Order, OrderItem
from api_order.serializers import OrderSerializer
from .payment_system import payment_order


@extend_schema(tags=['Order'])
class OrderAPIView(APIView):

    serializer_class = OrderSerializer
    @extend_schema(operation_id='api_get_orders_list_unique')
    def get(self, request: Request) -> Response:
        """
        Получить список заказов.
        """

        orders = Order.objects.filter(user_id=request.user.pk).all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @extend_schema(operation_id='api_orders_create_unique')
    def post(self, request: Request) -> Response:
        """
        Создать новый заказ
        """

        data = request.data
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        if user:
            order = Order.objects.create(
                user_id=user.pk,
            )
        else:
            session_key = request.session.session_key
            if session_key is None:
                request.session.create()
                session_key = request.session.session_key
                order = Order.objects.create(
                    session_key=session_key
                )
            else:
                order = Order.objects.create(
                    session_key=session_key
                )

        for product in data:
            OrderItem.objects.create(
                order=order,
                product=Product.objects.filter(id=product['id']).first(),
                price=product['price'],
                count=product['count']
            )
        return Response({"orderId": order.pk})


@extend_schema(tags=['Order'])
class OrderItemsAPIViews(APIView):

    serializer_class = OrderSerializer

    def get(self, request: Request, pk: int) -> Response:
        """
        Отобразить детали заказа.
        """

        order = Order.objects.filter(pk=pk).first()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @extend_schema(operation_id='api_order_update_unique')
    def post(self, request: Request, pk: int) -> Response:
        """
        Обновление данных заказа.
        """

        data = request.data
        total_order_cost = float(data['totalCost'])
        order_id = str(pk)
        delivery_type = data['deliveryType']
        if delivery_type == 'express':
            total_order_cost += 500
        else:
            if total_order_cost < 2000:
                total_order_cost += 200
        Order.objects.filter(id=order_id).update(
            fullName=data['fullName'],
            email=data['email'],
            phone=data['phone'],
            deliveryType=delivery_type,
            total_order_cost=total_order_cost,
            paymentType=data['paymentType'],
            status=data['status'],
            city = data['city'],
            address = data['address'],
        )
        return Response({"orderId": order_id})


@extend_schema(tags=['Payment'])
class PaymentAPIView(APIView):

    serializer_class = EmptySerializer

    def post(self, request: Request, pk: int) -> Response:
        """
        Оплата заказа.
        """

        data = request.data
        payment_status = payment_order(
            order_id=pk,
            cart_number=data['number'],
            month=data['month'],
            year=data['year'],
            code_cvv=data['code']
        )
        if payment_status:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
