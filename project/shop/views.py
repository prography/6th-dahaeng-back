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

class ItemListView(APIView):
    permssion_classes = [MyIsAuthenticated, ]
    
    def get(self, request):
        User = get_user_model()
        email = request.user.email
        profile = User.objects.get(email=email)

        try:
            had_item_list = UserItem.objects.filter(profile=profile)
            had_items = Item.objects.filter(id__in=had_item_list)
            not_had_items = Item.objects.exclude(id__in=had_item_list)
        except UserItem.DoesNotExist:
            had_items = {}
            not_had_items = Item.objects.all()
            
        had_sz = ItemSerializer(had_items, many=True)
        not_had_sz = ItemSerializer(not_had_items, many=True)

        return Response({
            "had_items" : had_sz.data,
            "not_had_items" : not_had_sz.data
        })

class ItemCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'response': 'success',
                'message': '성공적으로 아이템을 업로드하였습니다.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            "response": "error", 
            "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailView(APIView):
    permission_classes = [MyIsAuthenticated, ]

    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except:
            raise Http404
    
    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        item = self.get_object(pk)
        price = item.item_price
        usercoin = UserCoin.objects.get(profile=request.user.pk)

        if usercoin.coin >= price:
            request.data['profile']=request.user.email
            serializer = UserItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                usercoin.coin -= price
                usercoin.save()
                return Response({
                    "reponse": "success",
                    "coin": usercoin.coin,
                    "message": "아이템을 성공적으로 구매했습니다."
                })
            return Response({
                "response": "error",
                "message": serializer.errors
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

        useritems = UserItem.objects.all().filter(profile=profile.pk)
        serializer = UserItemSerializer(useritems, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        profile = request.user
        colorId = request.data.get('color').get('id')
        item = Item.objects.get(id=colorId)
        
        # 조랭이 색 착용
        try:
            # 같은 타입의 다른 아이템 벗기
            try:
                useritem = UserItem.objects.filter(profile=profile.pk, item__item_type=item.item_type).exclude(item__item_detail=item.item_detail)
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