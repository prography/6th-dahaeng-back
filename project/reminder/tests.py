from rest_framework.test import APITestCase, APIClient
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Reminder
from record.models import Post
from unittest import skip


class ReminderTestCase(APITestCase):
    def setUp(self):
        self.email = "rkdalstjd9@naver.com"
        self.password = "qwe123"
        profile = get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )

    @skip
    def test_create_reminder(self):
        profile = get_user_model().objects.get(email=self.email)
        self.client.force_authenticate(user=profile)

        url = reverse("reminder")
        response = self.client.post(url)
        reminders = Reminder.objects.all()
        breakpoint()

    def test_get_today_reminder(self):
        profile = get_user_model().objects.get(email=self.email)
        self.client.force_authenticate(user=profile)

        post = Post.objects.create(
            profile=profile,
            detail="post의 detail",
            emotion="FUN"
        )

        reminders = [
            Reminder(post=post, interval=7),
            Reminder(post=post, interval=30)
        ]
        Reminder.objects.bulk_create(reminders)

        url = reverse("reminder")
        response = self.client.get(url)
        self.assertEqual(response.data['response'], 'success')
        self.assertEqual(len(response.data['message']), len(reminders))
