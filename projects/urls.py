from django.urls import path

from projects import views

app_name = "projects"

urlpatterns = [
    path("list/", views.project_list_view, name="project_list"),
    path("favorites/", views.favorite_projects_view, name="favorite_projects"),
    path("create-project/", views.create_project_view, name="project_create"),
    path("<int:project_id>/", views.project_detail_view,
         name="project_detail"),
    path("<int:project_id>/edit/", views.edit_project_view,
         name="project_edit"),
    path(
        "<int:project_id>/complete/",
        views.project_complete_view,
        name="project_complete",
    ),
    path(
        "<int:project_id>/toggle-participate/",
        views.project_toggle_participate_view,
        name="project_participate",
    ),
    path(
        "<int:project_id>/toggle-favorite/",
        views.project_toggle_favorite_view,
        name="project_favorite",
    ),
]
