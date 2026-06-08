import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from projects.forms import ProjectForm
from projects.models import Project
from core.service import paginate_queryset
from projects.constants import PAGE_SIZE
from .constants import PROJECT_STATUS_CLOSED, PROJECT_STATUS_OPEN


def project_list_view(request):
    projects = (
        Project.objects.select_related("owner")
        .prefetch_related("participants")
        .order_by("-created_at")
    )

    page_obj, query_prefix = paginate_queryset(projects, request, PAGE_SIZE)

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
            "page_obj": page_obj,
            "query_prefix": query_prefix,
        },
    )


def project_detail_view(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=project_id,
    )
    return render(request, "projects/project-details.html",
                  {"project": project})


@login_required
@require_POST
def project_complete_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user.id != project.owner_id or project.status != PROJECT_STATUS_OPEN:
        return JsonResponse({"status": "error"},
                            status=HTTPStatus.FORBIDDEN)

    project.status = PROJECT_STATUS_CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status":
                         PROJECT_STATUS_CLOSED})


@login_required
@require_POST
def project_toggle_participate_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user.id == project.owner_id:
        return JsonResponse({"status": "error"}, status=HTTPStatus.BAD_REQUEST)

    if is_participant := project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({"status": "ok", "participant": is_participant})


@login_required
@require_POST
def project_toggle_favorite_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if favorited := not request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.add(project)
    else:
        request.user.favorites.remove(project)

    return JsonResponse({"status": "ok", "favorited": favorited})


@login_required
def favorite_projects_view(request):
    projects = (
        request.user.favorites.select_related("owner")
        .prefetch_related("participants")
        .order_by("-created_at")
    )
    return render(request, "projects/favorite_projects.html",
                  {"projects": projects})


@login_required
def create_project_view(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect(reverse("projects:project_detail", args=[project.id]))

    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": False},
    )


@login_required
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user.id != project.owner_id and not request.user.is_staff:
        return redirect(reverse("projects:project_detail", args=[project.id]))

    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect(reverse("projects:project_detail", args=[project.id]))

    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True},
    )
