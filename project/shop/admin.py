from django.contrib import admin
from .models import Item, UserItem, Jorang


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(UserItem)
class UserItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Jorang)
class JorangAdmin(admin.ModelAdmin):
    pass