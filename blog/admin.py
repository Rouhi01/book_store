from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}