from rest_framework import serializers as sz
from shop.models import Items, UserItems
from core.models import Profile

class ItemSerializer(sz.ModelSerializer):
    class Meta:
        model = Items
        fields = [
            'id', 
            'item_type', 
            'item_detail', 
            'item_price', 
            'released_at'
        ]
        
    
class UserItemSerializer(sz.ModelSerializer):
    class Meta:
        model = UserItems
        fields = [
            'profile',
            'item',
            'is_worn'
        ]