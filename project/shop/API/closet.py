from rest_framework.views import APIView
from rest_framework.response import Response

from config.permissions import MyIsAuthenticated
from core.models import Jorang, Profile
from core.ERROR.error_cases import GlobalErrorMessage, GlobalErrorMessage400
from shop.models import Item, UserItem
from shop.serializers import UserItemSerializer


class MyClosetView(APIView):
    permission_classes = (MyIsAuthenticated,)

    def get(self, request):
        """
            user 가 구입을 했던 item 들을 list 에 넣어 돌려준다.
        """
        profile = Profile.objects.get(email=request.user.email)

        user_items = UserItem.objects.all().filter(profile=profile.pk)
        serializer = UserItemSerializer(user_items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            내가 샀던 Item 을 조랭이에게 입혀보는 기능이다.
        """
        profile = request.user
        color_id = request.data.get('color').get('item')
        try:
            item = Item.objects.get(id=color_id)
        except Item.DoesNotExist:
            raise GlobalErrorMessage('Item 이 DB에 존재 하지 않습니다.')
        user_item = None

        # 조랭이 색 착용
        # 같은 타입의 다른 아이템 벗기
        try:
            user_item = UserItem.objects.filter(profile=profile.pk, item__item_type=item.item_type).exclude(
                item__item_detail=item.item_detail)
            user_item.update(is_worn=False)
        except UserItem.DoesNotExist:
            pass

        try:
            user_color = UserItem.objects.get(profile=profile.pk, item=color_id)
            user_color.is_worn = True
            user_color.save()
        except UserItem.DoesNotExist:
            if user_item:
                user_item.update(is_worn=True)
            raise GlobalErrorMessage("해당 아이템이 없습니다.")

        try:
            jorang = Jorang.objects.get(profile=profile)
            jorang.color = item.item_detail
            jorang.save()
        except Jorang.DoesNotExist:
            raise GlobalErrorMessage400("조랭이가 없습니다. 조랭이를 먼저 생성하세요.")

        return Response({
            "response": "success",
            "message": "성공적으로 아이템을 착용하였습니다.",
            "item information": "%s (%s)" % (item.item_type, item.item_detail)
        })
