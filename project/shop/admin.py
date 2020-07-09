from django.contrib import admin
from .models import Items, UserItems

@admin.register(Items)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(UserItems)
class UserItemAdmin(admin.ModelAdmin):
    pass