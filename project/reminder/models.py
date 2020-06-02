from record.models import Post
from django.db import models


class Reminder(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    interval = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.profile}의 {self.post.created_at} remainder"

    class Meta:
        unique_together = ('post', 'interval')
