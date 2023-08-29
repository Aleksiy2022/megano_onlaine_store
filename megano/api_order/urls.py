from django.urls import path
from . import api_views

app_name = 'api_order'

urlpatterns = [
    path('api/orders', api_views.OrderAPIView.as_view()),
    path('api/orders/<int:pk>', api_views.OrderItemsAPIViews.as_view()),
    path('api/order/<int:pk>', api_views.OrderItemsAPIViews.as_view()),
    path('api/payment/<int:pk>', api_views.PaymentAPIView.as_view()),
]
