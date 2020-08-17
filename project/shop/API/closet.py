from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.contrib.auth import get_user_model
from config.permissions import MyIsAuthenticated
from core.models import UserCoin, Jorang
from core.serializers import UserCoinSerializer
from shop.models import Item, UserItem
from shop.serializers import ItemSerializer, UserItemSerializer


class MyClosetView(APIView):
    permission_classes = (MyIsAuthenticated,)

    def get(self, request):
        """
            user 가 구입을 했던 item 들을 list 에 넣어 돌려준다.
        """
        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)

        useritems = UserItem.objects.all().filter(profile=profile.pk)
        serializer = UserItemSerializer(useritems, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        profile = request.user
        colorId = request.data.get('color').get('item')
        item = Item.objects.get(id=colorId)

        # 조랭이 색 착용
        try:
            # 같은 타입의 다른 아이템 벗기
            try:
                useritem = UserItem.objects.filter(profile=profile.pk, item__item_type=item.item_type).exclude(
                    item__item_detail=item.item_detail)
                useritem.update(is_worn=False)
            except UserItem.DoesNotExist:
                pass

            try:
                usercolor = UserItem.objects.get(profile=profile.pk, item=colorId)
                usercolor.is_worn = True
                usercolor.save()
            except UserItem.DoesNotExist:
                return Response({
                    "response": "error",
                    "message": "해당 아이템이 없습니다."
                })

            jorang = Jorang.objects.get(profile=profile)
            jorang.color = item.item_detail
            jorang.save()

            return Response({
                "response": "success",
                "message": "성공적으로 아이템을 착용하였습니다.",
                "item information": "%s (%s)" % (item.item_type, item.item_detail)
            })
        except Jorang.DoesNotExist:
            return Response({
                'response': 'error',
                'message': '조랭이가 없습니다. 조랭이를 먼저 생성하세요.'
            }, status=status.HTTP_400_BAD_REQUEST)
