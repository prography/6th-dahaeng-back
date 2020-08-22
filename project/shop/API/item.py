from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from django.http import Http404
from config.permissions import MyIsAuthenticated
from core.ERROR.error_cases import GlobalErrorMessage
from core.models import UserCoin, Profile
from shop.models import Item, UserItem
from shop.serializers import ItemSerializer, UserItemSerializer


# /item/user/ GET
@api_view(['GET'])
@permission_classes([MyIsAuthenticated, ])
def get_item_list_user_had_or_not(request):
    """
        Get 을 통해서, 관리자가 만들어 둔 Item list 를 얻어 오고,
        user 가 가지고 있는 것과 비교를 하여,
        user 가 소유를 하고 있는 item list 와 user 가 소유하고 있지 않는 item list 를 찾아서 Return 한다.
    """

    email = request.user.email
    profile = Profile.objects.get(email=email)

    try:
        had_item_list = UserItem.objects.filter(profile=profile).values('item').distinct()
        had_items = Item.objects.filter(id__in=had_item_list)
        not_had_items = Item.objects.exclude(id__in=had_item_list)

    except UserItem.DoesNotExist:
        had_items = {}
        not_had_items = Item.objects.all()
    had_sz = ItemSerializer(had_items, many=True)
    not_had_sz = ItemSerializer(not_had_items, many=True)

    return Response({
        "had_items": had_sz.data,
        "not_had_items": not_had_sz.data
    })


# /item/create/ POST
@api_view(['POST'])
@permission_classes([IsAdminUser, ])  # IsAdminUser, MyIsAuthenticated
def admin_create_item(request):
    """
        Admin 이 아이템을 만들기위해서,
        구현된 API 이며,
        사실상 Admin 을 통해서 들어가서 수정을 할 일이 많다고 생각하고 있음.
    """
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


# /item/2
@api_view(['GET'])
@permission_classes([MyIsAuthenticated, ])  # IsAdminUser
def get_item_with_pk(request, pk):
    """
        Item 에 pk를 통해서 접근을 하여 해당 Item 을 돌려준다.
    """
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response({
            'response': 'error',
            'message': 'pk 에 해당하는 Item 이 없습니다.'
        })
    except:
        raise Http404
    serializer = ItemSerializer(item)
    return Response(serializer.data)


# /item/buy/
@api_view(['POST'])
@permission_classes([MyIsAuthenticated, ])
def user_buy_item(request):
    """
        Item 에 pk를 통해서 접근을 하여 해당 Item 을 돌려준다.
    """

    try:
        item_pk = int(request.data["item"])
    except KeyError:
        raise GlobalErrorMessage('item : pk 가 존재 하지 않습니다.')

    except ValueError:
        raise GlobalErrorMessage('pk에 숫자가 들어 있지 않습니다.')

    try:
        item = Item.objects.get(pk=item_pk)
    except Item.DoesNotExist:
        raise GlobalErrorMessage('pk 에 해당하는 Item 이 없습니다.')

    price = item.item_price
    user_coin = UserCoin.objects.get(profile=request.user.pk)

    if user_coin.coin >= price:
        request.data['profile'] = request.user.email
        serializer = UserItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_coin.coin -= price
            user_coin.save()
            return Response({
                "response": "success",
                "coin": user_coin.coin,
                "message": "아이템을 성공적으로 구매했습니다."
            })
        raise GlobalErrorMessage(str(serializer.errors))

    raise GlobalErrorMessage("코인이 부족합니다.")
