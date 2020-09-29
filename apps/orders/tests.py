import json
from django.contrib.auth import get_user_model as user_model
User = user_model()
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .serializers import CustomerSerializer, OrderSerializer
from .models import Order

class CustomerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email = "customer@savinfo.app",
                                            first_name = "Customer",
                                            last_name = "Doe",
                                            phone_number = "+254722122122",
                                            password = "customer123")
        self.token = self.user.token
        self.api_authentication()

    def tearDown(self):
        User.objects.all().delete()        

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.token)

    def test_customers_view_is_admin(self):
        admin_user = User.objects.create_superuser(email = "superuser@savinfo.app",
                                                    first_name = "Superuser",
                                                    last_name = "Doe",
                                                    phone_number = "+254722122122",
                                                    password = "superuser123")
        self.client.force_authenticate(user=admin_user)
        response = self.client.get(reverse("customers-view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customers_view_not_admin(self):
        response = self.client.get(reverse("customers-view"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_customer_by_owner(self):        
        this_customer_id = self.user.id
        response = self.client.get(reverse("single-customer-view", kwargs={"pk": this_customer_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Customer")

    def test_get_single_customer_by_random_user(self):
        this_customer_id = self.user.id
        random_user = User.objects.create_user(email = "randomuser@savinfo.app",
                                                first_name = "Randomuser",
                                                last_name = "Doe",
                                                phone_number = "+254722133133",
                                                password = "randomuser123")
        self.client.force_authenticate(user=random_user)
        response = self.client.get(reverse("single-customer-view", kwargs={"pk": this_customer_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_single_customer_by_owner(self):
        this_customer_id = self.user.id
        response = self.client.put(reverse("single-customer-view", kwargs={"pk": this_customer_id}),
                                    {"first_name": "NewCustomer", "last_name": "NewDoe"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                        {"id": this_customer_id,
                        "email": "customer@savinfo.app",
                        "first_name": "NewCustomer",
                        "last_name": "NewDoe",
                        "phone_number": "+254722122122"})

    def test_update_single_customer_by_random_user(self):
        this_customer_id = self.user.id
        random_user = User.objects.create_user(email = "randomuser@savinfo.app",
                                                first_name = "Randomuser",
                                                last_name = "Doe",
                                                phone_number = "+254722133133",
                                                password = "randomuser123")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse("single-customer-view", kwargs={"pk": this_customer_id}),
                                    {"first_name": "HackedCustomer", "last_name": "HackedDoe"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_single_customer_by_owner(self):
        this_customer_id = self.user.id
        response = self.client.delete(reverse("single-customer-view", kwargs={"pk": this_customer_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

    def test_delete_single_customer_by_random_user(self):
        this_customer_id = self.user.id
        random_user = User.objects.create_user(email = "randomuser@savinfo.app",
                                                first_name = "Randomuser",
                                                last_name = "Doe",
                                                phone_number = "+254722133133",
                                                password = "randomuser123")
        self.client.force_authenticate(user=random_user)
        response = self.client.delete(reverse("single-customer-view", kwargs={"pk": this_customer_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        

       

class OrderTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email = "customer@savinfo.app",
                                            first_name = "Customer",
                                            last_name = "Doe",
                                            phone_number = "+254722122122",
                                            password = "customer123")
        self.token = self.user.token
        self.api_authentication()

        self.order = Order.objects.create(item = "pens", amount=5, customer=self.user)

    def tearDown(self):
        User.objects.all().delete()
        Order.objects.all().delete()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.token)

    def test_get_all_orders_is_admin(self):
        admin_user = User.objects.create_superuser(email = "superuser@savinfo.app",
                                                    first_name = "Superuser",
                                                    last_name = "Doe",
                                                    phone_number = "+254722122122",
                                                    password = "superuser123")
        self.client.force_authenticate(user=admin_user)
        response = self.client.get(reverse("all-orders-view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_orders_not_admin(self):
        response = self.client.get(reverse("all-orders-view"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_order(self):
        data = {"item": "books",                               
                "amount": 50}
        response = self.client.post(reverse("make-order-view"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["item"], "books")
        self.assertEqual(response.data["amount"], 50)

    def test_get_customer_orders_by_owner(self):        
        this_customer_id = self.user.id
        response = self.client.get(reverse("customer-orders-view", kwargs={"pk": this_customer_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_orders_by_random_user(self):        
        this_customer_id = self.user.id
        random_user = User.objects.create_user(email = "randomuser@savinfo.app",
                                                first_name = "Randomuser",
                                                last_name = "Doe",
                                                phone_number = "+254722133133",
                                                password = "randomuser123")
        self.client.force_authenticate(user=random_user)
        response = self.client.get(reverse("customer-orders-view", kwargs={"pk": this_customer_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  
        
    def test_get_single_order_by_owner(self):        
        this_order_id = self.order.id
        response = self.client.get(reverse("single-order-view", kwargs={"pk": this_order_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["item"], "pens")

    def test_get_single_order_by_random_user(self):
        this_order_id = self.order.id
        random_user = User.objects.create_user(email = "randomuser@savinfo.app",
                                                first_name = "Randomuser",
                                                last_name = "Doe",
                                                phone_number = "+254722133133",
                                                password = "randomuser123")
        self.client.force_authenticate(user=random_user)
        response = self.client.get(reverse("single-order-view", kwargs={"pk": this_order_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_single_order_by_owner(self):
        this_order_id = self.order.id
        response = self.client.put(reverse("single-order-view", kwargs={"pk": this_order_id}),
                                    {"amount": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], 10)
                        

    def test_update_single_order_by_random_user(self):
        this_order_id = self.order.id
        random_user = User.objects.create_user(email = "randomuser@savinfo.app",
                                                first_name = "Randomuser",
                                                last_name = "Doe",
                                                phone_number = "+254722133133",
                                                password = "randomuser123")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse("single-order-view", kwargs={"pk": this_order_id}),
                                    {"amount": 100000})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_single_order_is_admin(self):
        this_order_id = self.order.id
        admin_user = User.objects.create_superuser(email = "superuser@savinfo.app",
                                                    first_name = "Superuser",
                                                    last_name = "Doe",
                                                    phone_number = "+254722122122",
                                                    password = "superuser123")
        self.client.force_authenticate(user=admin_user)
        response = self.client.delete(reverse("single-order-view", kwargs={"pk": this_order_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_single_order_not_admin(self):
        this_order_id = self.order.id
        response = self.client.delete(reverse("single-order-view", kwargs={"pk": this_order_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 

    