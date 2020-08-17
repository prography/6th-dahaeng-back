"""
ItemDetail 에 왜 POST 를 사용을 하고 있는 걸까?
사실상 Class 로 모아서 처리를 하고 싶었지만, 현실적으로는 함수간의 naming 적인 연관성을 없애는 행동이라 생각하고,
FBV 로 사용하는게 더 네이밍에 맞다고 생각합니다. (적어도 ItemDetailView 는 보면서 이상하다는 생각)

요약 -> naming 에 맞는 기능으로 바꾸어 나가자.


원래
    path('', views.ItemListView.as_view(), name='item_list'),
    path('newitem/', views.ItemCreateView.as_view(), name='item_create'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),

현재
    '/item/user/' GET 으로 Item 의 user 가 Item list 중 각각 item 을 가지고 있는지 아닌지에 대해서 각각의 List 를 돌려준다.
    '/item/create/' POST 로 '관리자'만, 접근을 하여 새로운 Item 을 만들수 있다. -> FBV
    '/item/<int:pk>/' 특정한 item 에 접근을 할 수 있도록 한다. -> FBV
    '/item/buy/<int:pk>/' 특정한 Item 을 구매를 할수 있도록 한다. -> FBV 이부분은 FBV 로 하게 될 경우, 굳이 pk 를 사용을
    할필요가 없는데, TODO: 이부분은 건의를 해봐야 겠다.






"""
from django.urls import path
from .API import item
from .API import closet

urlpatterns = [
    path('item/user/', item.get_item_list_user_had_or_not, name='item_user_list'),
    path('item/create/', item.admin_create_item, name='item_create'),
    path('item/<int:pk>/', item.get_item_with_pk, name='item_detail'),
    path('item/buy/', item.user_buy_item, name='item_user_buy'),
    path('mycloset/', closet.MyClosetView.as_view(), name='closet_list'),
    # path('item/buy/<int:pk>/', item.user_buy_item, name='item_user_buy'),


    # path('', views.ItemListView.as_view(), name='item_list'),
    # path('newitem/', views.ItemCreateView.as_view(), name='item_create'),
    # path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    # path('mycloset/', views.MyClosetView.as_view(), name='closet_list'),
]
