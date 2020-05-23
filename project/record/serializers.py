from rest_framework import serializers as sz
from .models import Post

class PostSerializer(sz.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')

class QuestionSerializer(sz.ModelSerializer):
    class Meta:
        fields = ('question')