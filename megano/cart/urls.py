from django.urls import path

from cart.api_views import CartAPIView

app_name = 'cart'

urlpatterns = (
    path('api/basket', CartAPIView.as_view()),
)