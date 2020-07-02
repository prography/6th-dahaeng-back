from rest_framework import serializers as sz
from record.models import Post, Question, UserQuestion
from core.models import Profile
from record.relations import QuestionRelatedField

from datetime import date


class QuestionSerializer(sz.ModelSerializer):
    content = sz.CharField(max_length=512)

    class Meta:
        model = Question
        fields = ['id', 'content']


class PostSerializer(sz.ModelSerializer):
    profile = sz.SlugRelatedField(
        queryset=Profile.objects.all(), slug_field='email',)
    emotion = sz.ChoiceField(choices=Post.EMOTION_CHOICES)
    question = sz.SlugRelatedField(
        queryset=Question.objects.all(), slug_field='content')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        today = date.today()
        created_at = instance.created_at
        if not today == created_at:
            raise sz.ValidationError(
                {"response": "error", "message": "지난 날짜는 수정할 수 없습니다."})
        else:
            instance.image = validated_data.get('image', instance.image)
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
            'image',
            'continuity',
        ]


class UserQuestionSerializer(sz.ModelSerializer):
    profile = sz.SlugRelatedField(
        queryset=Profile.objects.all(), slug_field='email',)
    question = QuestionRelatedField(
        queryset=Question.objects.all(), slug_field='id')

    def create(self, validated_data):
        return UserQuestion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.last_login = validated_data.get(
            'last_login', instance.last_login)
        instance.question = validated_data.get('question', instance.question)
        instance.save()
        return instance

    class Meta:
        model = UserQuestion
        fields = ('profile', 'last_login', 'question')
