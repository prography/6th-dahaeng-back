from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ProfileSerializer


def main(request):
    return HttpResponse("hello world")


class CreateProfileView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        {
            "profile": {
                "username": "rkdalstjd9",
                "password": "qwe123",
                "email": "rkdalstjd9@naver.com",
                "nickname": "arkss"
            }
        }
        """
        data = request.data.get('profile')
        if not data:
            return Response({
                'response': 'error',
                'message': 'profile 파라미터가 없습니다.'
            })
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            profile = serializer.save()
        else:
            return Response({
                'response': 'error',
                'message': serializer.errors
            })

        return Response({
            'response': 'success',
            'message': serializer.data
        })
