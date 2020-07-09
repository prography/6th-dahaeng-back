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
    profile = sz.SlugRelatedField(
        queryset=Profile.objects.all(), slug_field='email',)
    
    def update(self, instance, validated_data):
        instance.is_worn = validated_data.get('is_worn', instance.is_worn)
        return instance
        
    class Meta:
        model = UserItems
        fields = [
            'id',
            'profile',
            'item',
            'is_worn'
        ]