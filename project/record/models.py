from django.db import models
from django.utils import timezone
from core.models import Profile

class Question(models.Model):
    question = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return '%s' % (self.question)

#class Emotion(models.Model):
    #emoji = models.CharField(max_length=50)
    
class Post(models.Model):
    EMOTION_CHOICES = [
        ('WARM',      "따뜻했어요"), 
        ('FUN',       "즐거웠어요"), 
        ('HAPPY',     "기뻤어요"), 
        ('TOUCHED',   "감동이에요"), 
        ('EXTRA',     "기타")
    ]

    created_at = models.DateField(auto_now_add=True)
    emotion = models.CharField(max_length=10, choices=EMOTION_CHOICES, default="WARM")
    question = models.CharField(max_length=512, blank=False)
    detail = models.TextField(blank=True)
    profile = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('created_at', 'profile')
        ordering = ('-created_at',)