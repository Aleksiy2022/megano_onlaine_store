from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api_catalog.models import Product
from api_order.models import Order, OrderItem
from api_order.serializers import OrderSerializer
from .payment_system import payment_order


class OrderListAPIView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.pk, paid=True).all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
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

class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = Order.objects.filter(pk=pk).first()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class OrderItemsAPIViews(APIView):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request, pk):
        data = request.data
        total_order_cost = float(data['totalCost'])
        order_id = data['orderId']
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


class PaymentAPIView(APIView):
    def post(self, request, pk):
        data = request.data
        payment_order(
            order_id=pk,
            cart_number=data['number'],
            month=data['month'],
            year=data['year'],
            code_cvv=data['code']
        )
        return Response(status=status.HTTP_200_OK)
