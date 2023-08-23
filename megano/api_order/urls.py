from django.urls import path
from .api_views import OrderListAPIView, OrderDetailAPIView, OrderItemsAPIViews, PaymentAPIView

app_name = 'api_order'

urlpatterns = [
    path('api/orders', OrderListAPIView.as_view()),
    path('api/orders/<int:pk>', OrderDetailAPIView.as_view()),
    path('api/order/<int:pk>', OrderItemsAPIViews.as_view()),
    path('api/payment', PaymentAPIView.as_view()),
    path('api/payment/<int:pk>', PaymentAPIView.as_view()),
]
