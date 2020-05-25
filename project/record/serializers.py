from rest_framework import serializers as sz
from .models import Post, Question
from core.models import Profile

class QuestionSerializer(sz.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question']

class PostSerializer(sz.ModelSerializer):
    
    profile = sz.SlugRelatedField(queryset=Profile.objects.all(), slug_field='email',)
    detail = sz.CharField(max_length=1000, style={'base_template': 'textarea.html'})
    question = sz.CharField(max_length=512) # manual
    emotion = sz.ChoiceField(choices=Post.EMOTION_CHOICES, default='따')
    
    def create(self, validated_data):
        """
        Create and return a new 'Post', given the validated data
        """
        post = Post.objects.create(**validated_data)
        return post
    
    def update(self, instance, validated_data):
        instance.detail = validated_data.get('detail', instance.detail)
        instance.save()
        return instance
    
    class Meta:
        model = Post
        fields = ['id', 'created_at', 'question', 'detail', 'profile', 'emotion'] #'image' 
        read_only_fields = ('question', )