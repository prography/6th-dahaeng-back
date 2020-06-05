from rest_framework.test import APITestCase, APIClient
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest import skip


class JorangTestCase(APITestCase):
    def setUp(self):
        email = "rkdalstjd9@naver.com"
        password = "qwe123"
        profile = get_user_model().objects.create_user(
            email=email,
            password=password
        )

    def test_create_jorang(self):
        self.client.login(email=self.email, password=self.password)
        url = reverse("jorang_create")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
