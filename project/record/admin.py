from django.contrib import admin
from .models import Post, Question


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class PostAdmin(admin.ModelAdmin):
    pass
