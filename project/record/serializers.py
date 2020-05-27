from rest_framework import serializers as sz
from .models import Post, Question
from core.models import Profile

from datetime import date

class QuestionSerializer(sz.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question']

class PostSerializer(sz.ModelSerializer):
    
    profile = sz.SlugRelatedField(queryset=Profile.objects.all(), slug_field='email',)
    emotion = sz.ChoiceField(choices=Post.EMOTION_CHOICES, default='따')
    created_at = sz.DateField(default=date.today())
    
    def validate(self, data):
        today = date.today()        
        if not today == data['created_at']:
            raise sz.ValidationError("지난 날짜는 수정할 수 없습니다.")
        return data

    def create(self, validated_data):
        """
        Create and return a new 'Post', given the validated data
        """
        post = Post.objects.create(**validated_data)
        return post
    
    def update(self, instance, validated_data):
        instance.emotion = validated_data.get('emotion', instance.emotion)
        instance.question = validated_data.get('question', instance.question)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.save()
        return instance
    
    class Meta:
        model = Post
        fields = [
            'id', 
            'created_at', 
            'question', 
            'detail', 
            'profile', 
            'emotion'
        ]