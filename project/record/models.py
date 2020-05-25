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
    EMOTION_CHOICES = (
        ('따', "따뜻했어요"), 
        ('즐', "즐거웠어요"), 
        ('기', "기뻤어요"), 
        ('감', "감동이에요"), 
        ('기', "기타")
    )

    created_at = models.DateField(auto_now_add=True)
    emotion = models.CharField(max_length=2, choices=EMOTION_CHOICES, default="따")
    #question = models.ManyToManyField(Question)
    question = models.CharField(max_length=512, blank=False)
    detail = models.TextField(blank=True)
    #image = models.ImageField(default='media/default_image.jpeg', upload_to=None, height_field=None, width_field=None, max_length=None)
    profile = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('created_at', 'profile')
        ordering = ('-created_at',)