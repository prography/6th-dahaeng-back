from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from record.models import Post, Question, UserQuestion
from record.serializers import PostSerializer, QuestionSerializer, UserQuestionSerializer
from record.filters import DynamicSearchFilter
from config.permissions import MyIsAuthenticated
from core.models import UserCoin
from core.serializers import UserCoinSerializer

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# random happy-question
import random
from datetime import date, timedelta
from calendar import monthrange

def pick_number():
    count = Question.objects.all().count()
    if count < 1:
        return 0
    return random.randint(1, count)

class PostList(ListAPIView):
    """
    List all happy-record of a now-user
    """
    permission_classes = [MyIsAuthenticated, ]
    serializer_class = PostSerializer
    filter_backends = (DynamicSearchFilter, )

    def get_queryset(self):
        return Post.objects.all().filter(profile=self.request.user.pk)

class PostCreateView(APIView):
    permission_classes = [MyIsAuthenticated, ]
    parser_classes = (FormParser, MultiPartParser,)
    
    def get(self, request):
        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)
        userquestion = UserQuestion.objects.get(profile=profile.pk)
    
        if userquestion.last_login is None or userquestion.last_login != date.today() or userquestion.question is None:
            qid = pick_number()
            qobj = get_object_or_404(Question, pk=qid)
            serializer = UserQuestionSerializer(
                userquestion,
                data={"last_login": date.today(), "question": qid},
                partial=True)
            if serializer.is_valid():
                serializer.save()

        question = UserQuestion.objects.filter(profile=request.user.pk)
        sz = UserQuestionSerializer(question, many=True)
        return Response(sz.data)
    
    def post(self, request):
        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)

        data = request.data
        _mutable = data._mutable
        data._mutable = True
        data['profile'] = email
        data['question'] = UserQuestion.objects.get(profile=request.user.pk).question

        today = date.today()            
        yesterday = today - timedelta(days=1)

        try:
            lastPost = Post.objects.get(profile=profile.pk, created_at=yesterday)
            continuity = Post.objects.get(profile=profile.pk, created_at=yesterday).continuity + 1
        except Post.DoesNotExist:
            continuity = 1

        if today.weekday() == 6:
            if continuity == 7:
                reward = 50
            elif continuity == monthrange(today.year, today.month)[1]:
                reward = 150
            else:
                reward = 10
        elif continuity == monthrange(today.year, today.month)[1]:
            reward = 50
            continuity = 0
        else:
            reward = 10
        data['continuity'] = continuity
        data._mutable = _mutable

        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            usercoin = UserCoin.objects.get(profile=profile.pk)
            uc_serializer = UserCoinSerializer(
                usercoin, data={'coin':usercoin.coin + reward}, partial=True)
            if uc_serializer.is_valid():
                uc_serializer.save()
            return Response({
                "response": "success", 
                "message": "성공적으로 일기를 업로드하였습니다."
                }, status=status.HTTP_201_CREATED)
        return Response({
            "response": "error",
            "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    """
    Retrieve a happy-record instance for a specific date
    """
    permission_classes = [MyIsAuthenticated, ]
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success", 
                "message": "성공적으로 수정하였습니다."})
        return Response({
            "response": "error", 
            "message" : serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# TODO
# permission_classes = [IsAdminUser, ]
class QuestionList(APIView):
    permission_classes = [MyIsAuthenticated, ]

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success",
                "message": "성공적으로 질문을 업로드하였습니다."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)