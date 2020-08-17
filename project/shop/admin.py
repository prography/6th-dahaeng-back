from django.contrib import admin
from .models import Item, UserItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(UserItem)
class UserItemAdmin(admin.ModelAdmin):
    pass
