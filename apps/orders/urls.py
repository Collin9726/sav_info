from django.urls import path, include
from .views import CustomersView, CustomerOrdersView, SingleCustomerView, AllOrdersView, SingleOrderView, MakeOrderView

urlpatterns = [
  path('customer/all/', CustomersView.as_view(),name = "customers-view"),
  path('customer/<int:pk>/', SingleCustomerView.as_view(), name = "single-customer-view"),
  path('customer/<int:pk>/orders/', CustomerOrdersView.as_view(), name = "customer-orders-view"),
  path('order/all/', AllOrdersView.as_view(), name = "all-orders-view"),
  path('order/<int:pk>/', SingleOrderView.as_view(), name = "single-order-view"),
  path('order/post/', MakeOrderView.as_view(), name = "make-order-view"),
]