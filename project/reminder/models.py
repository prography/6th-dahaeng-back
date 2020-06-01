from record.models import Post
from django.db import models


class Reminder(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post.profile}의 {self.post.created_at} remainder"
