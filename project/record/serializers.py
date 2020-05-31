from rest_framework import serializers as sz
from record.models import Post, Question
from core.models import Profile
from record.relations import QuestionRelatedField

from datetime import date

class QuestionSerializer(sz.ModelSerializer):
    content = sz.CharField(max_length=512)

    class Meta:
        model = Question
        fields = ['id', 'content']

class PostSerializer(sz.ModelSerializer):
    profile = sz.SlugRelatedField(queryset=Profile.objects.all(), slug_field='email',)
    emotion = sz.ChoiceField(choices=Post.EMOTION_CHOICES)
    question = QuestionRelatedField(queryset=Question.objects.all(), slug_field='id')
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        today = date.today()
        created_at = instance.created_at
        if not today == created_at:
            raise sz.ValidationError({"response": "error", "message": "지난 날짜는 수정할 수 없습니다."})
        else:
            instance.emotion = validated_data.get('emotion', instance.emotion)
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
            'emotion',
        ]