from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.contrib.auth import get_user_model
from config.permissions import MyIsAuthenticated
from core.models import UserCoin, Jorang
from core.serializers import UserCoinSerializer
from shop.models import Items, UserItems
from shop.serializers import ItemSerializer, UserItemSerializer

class ItemListView(ListAPIView):
    permssion_classes = [MyIsAuthenticated, ]
    serializer_class = ItemSerializer
    
    def get_queryset(self):
        return Items.objects.all()

class ItemDetailView(APIView):
    permission_classes = [MyIsAuthenticated, ]

    def get_object(self, pk):
        try:
            return Items.objects.get(pk=pk)
        except:
            raise Http404
    
    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        item = self.get_object(pk)
        price = item.item_price

        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)
        usercoin = UserCoin.objects.get(profile=profile.pk)

        if usercoin.coin >= price:
            data = request.data
            data['profile'] = email
            data['item'] = pk
            serializer = UserItemSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                usercoin.coin -= price
                usercoin.update()
                return Response({
                    "reponse": "success",
                    "coin": usercoin.coin,
                    "message": "아이템을 성공적으로 구매했습니다."
                })
            return Response({
                "response": "error",
                "message": serializer.error
            })
        else:
            return Response({
                "response": "error",
                "message": "코인이 부족합니다."
            })

class MyClosetView(APIView):
    permission_classes = (MyIsAuthenticated, )

    def get(self, request):
        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)

        useritems = UserItems.objects.all().filter(profile=profile.pk)
        serializer = UserItemSerializer(useritems, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        profile = request.user
        colorId = request.data.get('color').get('id')

        try:
            jorang = Jorang.objects.get(profile=profile)
            try:
                useritem = UserItems.objects.get(profile=profile.pk, item__item_detail=colorId)
                item_type = useritem.item_type
                useritem.is_worn = True
                useritem.save()
            except UserItems.DoesNotExist:
                return Response({
                    'response': 'error',
                    'message': '헤당 아이템이 존재하지 않습니다.'
                })
                
            try:
                useritem = UserItems.objects.exclude(profile=profile.pk, item__item_detail=colorId).filter(profile=profile.pk, item__item_type=item_type)
                useritem.update(is_worn=False)
            except UserItems.DoesNotExist:
                pass
        except Jorang.DoesNotExist:
            return Response({
                'response': 'error',
                'message': '조랭이가 없습니다. 조랭이를 먼저 생성하세요.'
            })
