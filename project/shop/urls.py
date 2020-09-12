from django.urls import path
from .API import item
from .API import closet

urlpatterns = [
    # TODO : Item list 들을 보내주는 API 더 추가.

    # 유저가 아이템 리스트에 대해서, 현재 본인이 가지고 있고 없고를 List 로 돌려주는 용도이다.
    path('item/user/', item.get_item_list_user_had_or_not, name='item_user_list'),

    # 관리자가 아이템을 만드는 것을 의미합니다.
    path('item/create/', item.admin_create_item, name='item_create'),

    # pk를 통해서, 아이템에 접근을 합니다.
    path('item/<int:pk>/', item.get_item_with_pk, name='item_detail'),

    # 유저가 아이템을 삽니다.
    path('item/buy/', item.user_buy_item, name='item_user_buy'),

    # get 을 통해, user 가 가지고 있는 아이템 list 를 들고 오고,
    # post 를 통해서, user 가 가지고 있는 아이템을 조랭이에게 입힐 수 있다.
    path('mycloset/', closet.MyClosetView.as_view(), name='closet_list'),
]
