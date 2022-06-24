from django.urls import path
from . import views

urlpatterns = [
  path('', views.cart_and_checkout, name='cart'),
  path('checkout/', views.cart_and_checkout, name="checkout"),
  path('<str:pri>/<int:pk>/', views.add_to_cart, name='add_to_cart'),
]