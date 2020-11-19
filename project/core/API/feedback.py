from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from core.models import UserFeedback


@api_view(['POST'])
@permission_classes([AllowAny])
def get_user_feedback(request):
    feedback = request.data.get("feedback")
    if not feedback:
        return Response({
            'response': 'error',
            'message': 'feedback 이 존재 하지 않습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    UserFeedback.objects.create(feedback=feedback)
    return Response({
        'response': 'success',
        'message': '성공적으로 유저의 피드백을 저장하였습니다.'
    })
