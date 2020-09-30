import json
from django.contrib.auth import get_user_model as user_model
User = user_model()
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .serializers import RegistrationSerializer, LoginSerializer

class RegistrationTestCase(APITestCase):

    def setUp(self):
        data = {"email": "test@savinfo.app",
                "password": "password123",
                "confirm_password": "password123",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+254722100100"}
        response = self.client.post(reverse("signup"), data)        

    def test_registration(self):
        data = {"email": "test1@savinfo.app",
                "password": "password456",
                "confirm_password": "password456",
                "first_name": "Jane",
                "last_name": "Doe",
                "phone_number": "+254722101101"}
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_existing_email(self):
        data = {"email": "test@savinfo.app",
                "password": "password456",
                "confirm_password": "password456",
                "first_name": "Jane",
                "last_name": "Doe",
                "phone_number": "+254722101101"}
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_field(self):
        data = {"email": "test4@savinfo.app",
                "password": "password456",
                "confirm_password": "password456",
                "first_name": "Jane",
                "last_name": "Doe"}
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        data = {"email": "test@savinfo.app",
                "password": "password123"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid(self):
        data = {"email": "test@savinfo.app",
                "password": "password000"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)