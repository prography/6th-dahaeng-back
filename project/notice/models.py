from django.db import models
from core.models import Profile


class Notice(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)


class Read(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
