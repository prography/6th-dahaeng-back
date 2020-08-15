import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Jorang
from rest_framework.decorators import api_view, permission_classes
from config.permissions import MyIsAuthenticated
from random import choice


def random_color():
    colors = ["FFE884", "FC9285", "8BAAD8", "F4E9DC", "BD97B4"]
    return choice(colors)


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
    # TODO: 내가 만든거 shop 을 구현을 하면, 그떄 추가로 구현 예정.
    """
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
    """

    return Response({
        'response': 'success',
        'message': 'Jorang이 성공적으로 생성되었습니다.'
    })
