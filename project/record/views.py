from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from record.models import Post, Question
from record.serializers import PostSerializer, QuestionSerializer
from record.filters import DynamicSearchFilter
from config.permissions import MyIsAuthenticated

from django.http import Http404

# random happy-question
import random

def pick_number():
    count = Question.objects.all().count()
    if count < 1:
        return 0
    return random.randint(1, count)

# TODO
# permission_classes = [MyIsAuthenticated, ]
class PostList(ListAPIView):
    """
    List all happy-record of a now-user
    """
    permission_classes = [AllowAny, ]
    serializer_class = PostSerializer
    filter_backends = (DynamicSearchFilter, )

    def get_queryset(self):
        return Post.objects.all().filter(profile=self.request.user.pk)

class PostCreateView(APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request):
        qid = pick_number()
        question = Question.objects.all().filter(id = qid)
        serializer = QuestionSerializer(question, many=True)
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.set_cookie('my_question', qid)
        return response
    
    def post(self, request):
        data = request.data
        data['profile'] = request.user.email
        data['question'] = request.COOKIES.get('my_question')
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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
    permission_classes = [AllowAny, ]
    
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
    permission_classes = [AllowAny, ]

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