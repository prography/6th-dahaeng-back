from django.test import TestCase, Client
from rest_framework.test import APIClient
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest import skip


class CreateProfileTest(TestCase):

    def setUp(self):
        self.email = 'rkdalstjd9@naver.com'
        self.password = "qwe123"
        self.valid_profile = {
            "profile": {
                "email": self.email,
                "password": self.password
            }
        }

    @skip
    def test_create_valid_profile(self):
        client = Client()
        response = client.post(
            reverse('signup'),
            data=json.dumps(self.valid_profile),
            content_type='application/json'
        )
        self.assertEqual(
            response.data['response'], 'success'
        )

    def create_user(self):
        User = get_user_model()
        email = self.email
        password = self.password
        profile = User(
            email=email,
            password=password
        )
        profile.status = '0'
        profile.role = '0'
        profile.save()
        return profile

    @skip
    def test_login_without_email_active(self):
        profile = self.create_user()
        client = Client()
        response = client.post(
            reverse('login'),
            data=json.dumps({
                "email": profile.email,
                "password": self.password
            }),
            content_type='application/json'
        )

        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    "Unable to log in with provided credentials."
                ]
            }
        )

    def test_login_with_email_active(self):
        profile = self.create_user()
        profile.status = '1'
        profile.save()

        client = APIClient()
        response = client.post(
            reverse('login'),
            data=json.dumps({
                "email": "rkdalstjd9@naver.com",
                "password": "qwe123"
                # "email": profile.email,
                # "password": self.password
            }),
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code,
            200
        )
