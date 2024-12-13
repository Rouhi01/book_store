from django.contrib import admin
from .forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'is_admin', 'is_active']
    list_filter = ['is_admin']

    # Corrected fieldsets
    fieldsets = (
        ('Main', {'fields': ['email', 'password']}),
        ('Permissions', {'fields': ['is_active', 'is_admin']}),
    )

    # Corrected add_fieldsets
    add_fieldsets = (
        ('Change', {
            'fields': ['email', 'p1', 'p2'],
        }),
    )

    search_fields = ['email']
    ordering = []
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
