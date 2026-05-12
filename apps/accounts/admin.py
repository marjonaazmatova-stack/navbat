"""Django Admin uchun foydalanuvchi sozlamalari."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Foydalanuvchilar admin paneli."""

    list_display = ('phone', 'full_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('phone', 'full_name', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ("Shaxsiy ma'lumotlar", {'fields': ('full_name', 'email', 'role')}),
        ('Huquqlar', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Muhim sanalar', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'role', 'password1', 'password2'),
        }),
    )
