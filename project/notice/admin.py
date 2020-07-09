from django.contrib import admin
from .models import Notice, Read


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass


@admin.register(Read)
class ReadAdmin(admin.ModelAdmin):
    pass
