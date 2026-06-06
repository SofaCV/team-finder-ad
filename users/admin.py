from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Skill, User


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "name", "surname", "phone", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", "name", "surname", "phone")
    ordering = ("-id",)
    filter_horizontal = ("skills", "favorites", "groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональные данные", {"fields": ("name", "surname", "avatar", "about", "phone", "github_url")}),
        ("Навыки и избранное", {"fields": ("skills", "favorites")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "surname", "password1", "password2", "phone"),
            },
        ),
    )
