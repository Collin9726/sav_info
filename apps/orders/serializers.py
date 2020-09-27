from rest_framework import serializers
from django.contrib.auth import get_user_model as user_model
User = user_model()
from .models import Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','phone_number',)

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    
    class Meta:
        model = Order
        fields = '__all__'
