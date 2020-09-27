from django.urls import path, include
from .views import CustomersView, CustomerOrdersView, SingleCustomerView, AllOrdersView, SingleOrderView, MakeOrderView

urlpatterns = [
  path('customer/all/', CustomersView.as_view()),
  path('customer/<int:pk>/', SingleCustomerView.as_view()),
  path('customer/<int:pk>/orders/', CustomerOrdersView.as_view()),
  path('order/all/', AllOrdersView.as_view()),
  path('order/<int:pk>/', SingleOrderView.as_view()),
  path('order/post/', MakeOrderView.as_view()),
]