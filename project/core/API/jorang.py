"""
조랭이 모델을 Create 하는 함수들이 정의 되어있습니다.
조랭이의 세부적인 내용을 추가하는 경우
profile.py 에서 ProfileDetail 부분을 참고하면 되겠습니다.

"""
from random import choice

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from core.models import Jorang
from config.permissions import MyIsAuthenticated
from shop.models import Item
from shop.serializers import UserItemSerializer


def random_color():
    colors = ["FFE884", "FC9285", "8BAAD8", "F4E9DC", "BD97B4"]
    return choice(colors)

# /jorang/
@api_view(['POST'])
@permission_classes([MyIsAuthenticated, ])
def create(request):
    """
        우리의 마스코트 조랭이
        조랭이의 경우, 생성될 때, 유저와 1:1 [OneToOneField] 로 mapping 이 되기 떄문에
        유저(Profile) 당 딱 한번 밖에 생성이 되지 않는다.
        그렇기에 유의를 할 필요가 있다.
        {
            "nickname": "산림수"
        }
    """
    try:
        nickname = request.data['nickname']
    except KeyError:
        return Response({
            'response': 'error',
            'message': 'request body의 파라미터가 잘못되었습니다.'
        })
    profile = request.user
    color = random_color()
    try:
        Jorang.objects.create(
            nickname=nickname,
            color=color,
            profile=profile
        )
    except Exception as e:
        if "UNIQUE constraint failed: core_jorang.profile_id" == str(e):
            return Response({
                'response': 'fail',
                'message': '이미 조랭이를 가지고 있는 계정입니다.'
            })
        print(e)
        # TODO : 정확한 이유를 파악을 할 수는 없지만, 만약 이런 경우가 생길 경우, 문제점을 파악하고 해결해야한다.
        return Response({
            'response': 'fail',
            'message': '조랭이 생성에 실패햐였습니다.'
        })

    # 개인 아이템 소지 목록에 색 추가
    try:
        item_id = Item.objects.get(
            item_type="jorang_color", item_detail=color).id
        serializer = UserItemSerializer(
            data={
                "profile": profile.email,
                "item": item_id,
                "is_worn": True
            })
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({
                "response": "error",
                "message": serializer.errors
            })
    except Item.DoesNotExist:
        return Response({
            'response': 'error',
            'message': '존재하지 않는 조랭이 색입니다. 상점에 색 아이템을 추가하세요!'
        })


    return Response({
        'response': 'success',
        'message': 'Jorang이 성공적으로 생성되었습니다.'
    })
