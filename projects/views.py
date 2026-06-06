import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from projects.forms import ProjectForm
from projects.models import Project

PAGE_SIZE = 12


def _build_query_prefix(request):
    params = []
    for key, value in request.GET.items():
        if key == "page":
            continue
        params.append(f"{key}={value}")
    return "&".join(params) + ("&" if params else "")


def project_list_view(request):
    projects = Project.objects.select_related("owner").prefetch_related(
        "participants"
    ).order_by("-created_at")
    paginator = Paginator(projects, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
            "page_obj": page_obj,
            "query_prefix": _build_query_prefix(request),
        },
    )


def project_detail_view(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=project_id,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
@require_POST
def project_complete_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user.id != project.owner_id or project.status != "open":
        return JsonResponse({"status": "error"}, status=403)
    project.status = "closed"
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": "closed"})


@login_required
@require_POST
def project_toggle_participate_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user.id == project.owner_id:
        return JsonResponse({"status": "error"}, status=400)
    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        return JsonResponse({"status": "ok", "participant": False})
    project.participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": True})


@login_required
@require_POST
def project_toggle_favorite_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({"status": "ok", "favorited": favorited})


@login_required
def favorite_projects_view(request):
    projects = request.user.favorites.select_related("owner").prefetch_related(
        "participants"
    ).order_by("-created_at")
    return render(request, "projects/favorite_projects.html", {"projects": projects})


@login_required
def create_project_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect(f"/projects/{project.id}/")
    else:
        form = ProjectForm()
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": False},
    )


@login_required
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user.id != project.owner_id and not request.user.is_staff:
        return redirect(f"/projects/{project.id}/")
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(f"/projects/{project.id}/")
    else:
        form = ProjectForm(instance=project)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True},
    )
