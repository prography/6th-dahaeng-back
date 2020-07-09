from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('newitem/', views.ItemCreateView.as_view(), name='item_create'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('mycloset/', views.MyClosetView.as_view(), name='closet_list'),
]
