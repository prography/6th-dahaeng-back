from rest_framework.test import APITestCase, APIClient
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Jorang
from ..views import get_or_none
from unittest import skip


class JorangTestCase(APITestCase):
    def setUp(self):
        self.email = "rkdalstjd9@naver.com"
        self.password = "qwe123"
        profile = get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )

    @skip
    def test_login(self):
        profile = get_user_model().objects.get(email="rkdalstjd9@naver.com")
        result = self.client.force_authenticate(user=profile)
        breakpoint()

    def test_check_has_jorang(self):
        profile = get_user_model().objects.get(email=self.email)
        Jorang.objects.create(
            nickname="조랭이 이름",
            color="000000",
            profile=profile
        )
        jorang = get_or_none(Jorang, profile=profile)
        if jorang is None:
            has_jorang = False
        else:
            has_jorang = True

        url = reverse("login")
        data = {
            "email": "rkdalstjd9@naver.com",
            "password": "qwe123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['message']['has_jorang'], has_jorang)

    def test_check_has_not_jorang(self):
        profile = get_user_model().objects.get(email=self.email)
        jorang = get_or_none(Jorang, profile=profile)
        if jorang is None:
            has_jorang = False
        else:
            has_jorang = True

        url = reverse("login")
        data = {
            "email": "rkdalstjd9@naver.com",
            "password": "qwe123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['message']['has_jorang'], has_jorang)

    def test_create_jorang(self):
        profile = get_user_model().objects.get(email=self.email)
        self.client.force_authenticate(user=profile)
        url = reverse("jorang_create")
        data = {
            "nickname": "산림수"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data["response"], "success")

    @skip
    def test_api_jwt(self):

        url = reverse('api-jwt-auth')
        u = user_model.objects.create_user(
            username='user', email='user@foo.com', password='pass')
        u.is_active = False
        u.save()

        resp = self.client.post(
            url, {'email': 'user@foo.com', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        u.is_active = True
        u.save()

        resp = self.client.post(
            url, {'username': 'user@foo.com', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']
        # print(token)

        verification_url = reverse('api-jwt-verify')
        resp = self.client.post(
            verification_url, {'token': token}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(
            verification_url, {'token': 'abc'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        resp = client.get('/api/v1/account/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        resp = client.get('/api/v1/account/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
