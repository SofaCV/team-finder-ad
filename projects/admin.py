from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "owner__email", "owner__name")
    filter_horizontal = ("participants",)
    raw_id_fields = ("owner",)
