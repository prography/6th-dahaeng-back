from django.db import models
from django.utils import timezone
from core.models import Profile

class Question(models.Model):
    question = models.CharField(max_length=512)

    def natural_key(self):
        return (self.question)

    def __str__(self):
        return '%s' % (self.question)

#class Emotion(models.Model):
    #emoji = models.CharField(max_length=50)
    
class Post(models.Model):
    created_at = models.DateField(auto_now_add=True)
    #emotion = models.CharField(max_length=50, blank=False)
    question = models.ManyToManyField(Question)
    answer = models.CharField(max_length=160) # 한글 80자
    detail = models.TextField(blank=True)
    #image = models.ImageField(default='media/default_image.jpeg', upload_to=None, height_field=None, width_field=None, max_length=None)
    profile = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('created_at', 'profile')
        ordering = ('-created_at',)

    def natural_key(self):
        return (self.question)