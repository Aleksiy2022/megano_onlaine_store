from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from api_auth.serializers import EmptySerializer
from api_order.models import Order
from api_order.serializers import OrderSerializer
from .payment_system import payment_order
from .tasks import create_order, update_order, order_payment_confirmation


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
            order = Order.objects.create(user_id=user.pk)
        else:
            request.session.create()
            session_key = request.session.session_key
            order = Order.objects.create(session_key=session_key)

        create_order.delay(request_data=data, order_id=order.pk)

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

        update_order.delay(order_id=str(pk), request_data=request.data, user_id=request.user.pk)
        return Response({"orderId": pk})


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
            user_id=request.user.pk
            order_payment_confirmation.delay(order_id=pk, user_id=user_id)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
