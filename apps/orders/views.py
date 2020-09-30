from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Order, User
from .serializers import OrderSerializer, CustomerSerializer
from .sms import SendSMS

# Create your views here.
class CustomersView(APIView):
    permission_classes = (IsAdminUser,)  

    def get(self, request, format=None):        
        all_customers = User.objects.filter(is_staff = False)
        serializers = CustomerSerializer(all_customers, many=True)
        return Response(serializers.data)     


class SingleCustomerView(APIView):
    permission_classes = (IsAuthenticated,)           
    
    def get_customer(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404()    

    def get(self, request, pk, format=None):
        this_customer = self.get_customer(pk)
        if request.user.is_staff:
            pass
        else:
            if request.user != this_customer:
                raise Http404()
              
        serializers = CustomerSerializer(this_customer)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        this_customer = self.get_customer(pk)
        if request.user.is_staff:
            pass
        else:
            if request.user != this_customer:
                raise Http404()        
        serializers = CustomerSerializer(this_customer, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk, format=None):
        this_customer = self.get_customer(pk)
        if request.user.is_staff:
            pass
        else:
            if request.user != this_customer:
                raise Http404()
        
        this_customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class AllOrdersView(APIView):
    permission_classes = (IsAdminUser,)  

    def get(self, request, format=None):        
        all_orders = Order.objects.all()
        serializers = OrderSerializer(all_orders, many=True)
        return Response(serializers.data) 


class CustomerOrdersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_customer(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404()  

    def get(self, request, pk, format=None):
        this_customer = self.get_customer(pk)
        if request.user.is_staff:
            pass
        else:
            if request.user != this_customer:
                raise Http404()

        orders_by_customer = Order.objects.filter(customer=this_customer)              
        serializers = OrderSerializer(orders_by_customer, many=True)
        return Response(serializers.data)

    

class SingleOrderView(APIView):
    permission_classes = (IsAuthenticated,)           
    
    def get_order(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404()    

    def get(self, request, pk, format=None):
        this_order = self.get_order(pk)
        if request.user.is_staff:
            pass
        else:
            if request.user != this_order.customer:
                raise Http404()
              
        serializers = OrderSerializer(this_order)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        this_order = self.get_order(pk)
        if request.user.is_staff:
            pass
        else:
            if request.user != this_order.customer:
                raise Http404()        
        serializers = OrderSerializer(this_order, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    

    def delete(self, request, pk, format=None):
        this_order = self.get_order(pk)
        if request.user.is_staff:
            pass
        else:            
            raise Http404()
        
        this_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MakeOrderView(APIView):
    permission_classes = (IsAuthenticated,)     

    def post(self, request, format=None):        
        serializers = OrderSerializer(data=request.data, partial=True)
        customer = request.user
        if serializers.is_valid():  
            order_item = serializers.validated_data['item']
            order_amount = serializers.validated_data['amount']          
            serializers.save(customer=customer)
            SendSMS(customer.first_name, customer.phone_number, order_item, order_amount)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

