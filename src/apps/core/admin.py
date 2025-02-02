from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User, Tag, Ingredient


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['name', 'user']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['name', 'user']
