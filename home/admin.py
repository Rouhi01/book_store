from django.contrib import admin
from .models import Comment, Like, Tag


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_model_name', 'object_id', 'content_object', 'created_at', 'is_reply']


admin.site.register(Like)
admin.site.register(Tag)
