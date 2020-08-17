from django.db.utils import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from record.models import Question
from record.serializers import QuestionSerializer
from config.permissions import MyIsAuthenticated


class QuestionView(APIView):
    """
        only 관리자들이 Question 들을 만들어서
        그것들을 질문 LIST 로 만드는 느낌이다.
    """

    permission_classes = [MyIsAuthenticated]
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        """
            Question 의 목록 전체를 가져와서,
            등록을 하는 과정을 가진다.
        """
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            새로운 Question 을 등록을 하는 과정입니다.
            {
                "content":"질문"
            }
        """
        try:
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "response": "success",
                    "message": "성공적으로 질문을 업로드하였습니다."
                }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({
                "response": "error",
                "message": "같은 질문을 Upload 하였습니다."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
