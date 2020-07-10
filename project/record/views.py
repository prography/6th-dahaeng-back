from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from record.models import Post, Question, UserQuestion
from record.serializers import PostSerializer, QuestionSerializer, UserQuestionSerializer
from record.filters import DynamicSearchFilter
from config.permissions import MyIsAuthenticated
from core.models import UserCoin, Attendance
from core.serializers import UserCoinSerializer

from django.http import Http404
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text

from random import randint
from datetime import date, timedelta
from calendar import monthrange

def pick_number():
    count = Question.objects.all().count()
    if count < 1:
        return 0
    return randint(1, count)

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

        # 하루에 한 개씩 행복 질문을 랜덤으로 생성
        if userquestion.question is None or userquestion.last_login != date.today() :
            qid = pick_number()
            try:
                question = Question.objects.get(pk=qid)
                serializer = UserQuestionSerializer(
                    userquestion,
                    data={"last_login": date.today(), "question": qid},
                    partial=True)
                if serializer.is_valid():
                    serializer.save()
            except Question.DoesNotExist:
                return Response({
                    "response": "error",
                    "message": "행복 질문이 존재하지 않습니다. 행복 질문 등록 후 이용하세요"
                    }, status=status.HTTP_400_BAD_REQUEST)

        question = UserQuestion.objects.filter(profile=request.user.pk)
        sz = UserQuestionSerializer(question, many=True)
        return Response(sz.data)
    
    def post(self, request):
        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)
        usercoin = UserCoin.objects.get(profile=profile.pk)

        data = request.data
        _mutable = data._mutable
        data._mutable = True
        data['profile'] = email
        data['question'] = UserQuestion.objects.get(profile=request.user.pk).question

        # 연속 기록 체크
        today = date.today()
        yesterday = today - timedelta(days=1)
        tommorow = today + timedelta(days=1)

        try:
            lastPost = Post.objects.get(profile=profile.pk, created_at=yesterday)
            continuity = lastPost.continuity + 1
        except Post.DoesNotExist:
            continuity = 1

        if continuity == 7:                                        # 7일 연속 기록 보상
            reward = 20
        elif continuity == 17:                                     # 17일 연속 기록 보상
            reward = 30
        elif continuity == 27:                                     # 27일 연속 기록 보상
            reward = 50
        elif continuity == monthrange(today.year, today.month)[1]: # 한 달 연속 기록 보상
            reward = 100
        else:                                                      # 기본 기록 보상
            reward = 10

        if today.month != tommorow.month:                          # 매 달 연속 기록 체크 초기화
            continuity = 0
        data['continuity'] = continuity
        data._mutable = _mutable
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            Attendance.objects.create(
                    profile=profile,
                    date=today,
                    emotion=data['emotion'])

            reward_of_today = usercoin.coin
            if usercoin.last_date is None:                         # 첫 일기 기록 보상
                reward_of_today = 100
            elif usercoin.last_date != today:                      # 하루 보상 제공 1회 제한
                reward_of_today += reward

            uc_serializer = UserCoinSerializer(
                                usercoin, 
                                data={"coin":reward_of_today, "last_date":today}, 
                                partial=True)
            if uc_serializer.is_valid():
                uc_serializer.save()
            
            post = Post.objects.get(profile=profile, created_at=today)
            return Response({
                "response": "success", 
                "message": "성공적으로 일기를 업로드하였습니다.",
                "post_detail": {
                    "id": post.id,
                    "created_at": post.created_at,
                    "detail": smart_text(post.detail, encoding='utf-16'),
                    "emotion": post.emotion,
                    "image": smart_text(post.image, encoding='utf-16'),
                },
                "reward_detail": {
                    "reward_of_today": reward,
                    "coin": reward_of_today,
                    "continuity": continuity
                }}, status=status.HTTP_201_CREATED)
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
        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)

        post = self.get_object(pk)
        serializer = PostSerializer(post)
        
        if post.profile == profile or profile.role == 10:
            return Response(serializer.data)
        else:
            return Response({
                'response': 'error',
                'message': '다른 사람의 일기는 볼 수 없어요.'
            })
    
    def patch(self, request, pk, format=None):
        post = self.get_object(pk)

        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)

        if post.profile == profile or profile.role == 10:
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
        else:
            return Response({
                'response': 'error',
                'message': '다른 사람의 일기는 수정할 수 없어요.'
            })

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)

        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)
        usercoin = UserCoin.objects.get(profile=profile.id)

        if post.profile == profile or profile.role == 10:
            if post.created_at == usercoin.last_date:
                return Response({
                    'response': 'error',
                    'message': '마지막 기록은 지울 수 없습니다.'
                })
            else:
                post.delete()
                return Response({
                    'response': 'success',
                    'message': '기록을 삭제하였습니다.'
                }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                'response': 'error',
                'message': '다른 사람의 일기는 삭제할 수 없어요.'
            })


class QuestionList(APIView):
    permission_classes = [IsAdminUser]

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