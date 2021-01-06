from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response

from config.permissions import MyIsAuthenticated
from core.models import Profile
from core.ERROR.error_cases import GlobalErrorMessage, GlobalErrorMessage400
from shop.models import Item, UserItem, Jorang
from shop.serializers import UserItemSerializer
from shop.API.request_format_serializers import MyClosetSerializer


class MyClosetView(APIView):
    permission_classes = (MyIsAuthenticated,)

    def get(self, request):
        """
            user 가 구입을 했던 item 들을 list 에 넣어 돌려준다.
        """
        user_items = UserItem.objects.all().filter(profile=request.user)
        serializer = UserItemSerializer(user_items, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=MyClosetSerializer,
        auth=None,
        tags=["A - New - Shop - POST MyCloset"],
        summary="POST MyCloset"
    )
    def post(self, request, format=None):
        """
            내가 샀던 Item 을 조랭이에게 입혀보는 기능이다.
        """
        profile = request.user
        wearing_item_id = request.data.get('item')

        try:
            item = Item.objects.get(id=wearing_item_id)
        except Item.DoesNotExist:
            raise GlobalErrorMessage('Item 이 DB에 존재 하지 않습니다.')

        wearing_item = None
        try:
            wearing_item = UserItem.objects.get(profile=profile, item=item)
        except UserItem.DoesNotExist:
            raise GlobalErrorMessage("해당 아이템이 없습니다.")

        jorang = None
        try:
            jorang = Jorang.objects.get(profile=profile)
        except Jorang.DoesNotExist:
            raise GlobalErrorMessage400("조랭이가 없습니다. 조랭이를 먼저 생성하세요.")

        # 같은 타입의 다른 아이템 벗기 (없으면 pass)
        try:
            worn_item = jorang.items.get(item__item_type=wearing_item.item.item_type)
            worn_item.is_worn = False
            worn_item.save()
            jorang.items.remove(worn_item)
        except UserItem.DoesNotExist:
            pass

        # 아이템 착용
        wearing_item.is_worn = True
        wearing_item.save()
        jorang.items.add(wearing_item)

        return Response({
            "response": "success",
            "message": "성공적으로 아이템을 착용하였습니다.",
            "item information": "%s (%s)" % (item.item_type, item.item_detail)
        })
