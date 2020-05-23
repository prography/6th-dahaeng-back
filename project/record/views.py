from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from .models import Post, Question
from .serializers import PostSerializer, QuestionSerializer
from config.permissions import MyIsAuthenticated

from django.http import Http404

# Restrict the post to be updated only on the day.
#from datetime import datetime
#from django.utils import timezone


class PostList(APIView):
    """
    List all happy-record of a now-user, or create a new happy-record
    """
    permssion_classes = [MyIsAuthenticated, ]

    def get(self, requeset, format=None):
        records = Post.objects.all()
        serializer = PostSerializer(records, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    """
    Retrieve a happy-record instance for a specific date
    """
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404
    def get(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = PostSerializer(record)
        return Response(serializer.data)
    
    # TODO
    # 같은 날짜에만 수정할 수 있도록 구현하기!!
    def put(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = PostSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class QuestionList(APIView):
    """
    List all happy-questions, or create a new happy-question
    """
    permssion_classes = [IsAdminUser, ]

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetail(APIView):
    """
    Retrieve, update or delete a happy-question.
    """
    permissions_classes = [IsAdminUser, ]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)