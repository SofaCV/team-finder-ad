import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from users.forms import (
    CustomPasswordChangeForm,
    EditProfileForm,
    LoginForm,
    RegistrationForm,
)
from users.models import Skill, User

PAGE_SIZE = 12


def _build_query_prefix(request, exclude=None):
    params = []
    for key, value in request.GET.items():
        if key == "page" or key in (exclude or []):
            continue
        params.append(f"{key}={value}")
    return "&".join(params) + ("&" if params else "")


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
            )
            login(request, user)
            return redirect("/projects/list/")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("/projects/list/")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/projects/list/")


def participants_list_view(request):
    participants = User.objects.filter(is_active=True).order_by("-id")
    active_skill = request.GET.get("skill", "")
    if active_skill:
        participants = participants.filter(skills__name=active_skill).distinct()
    all_skills = (
        Skill.objects.order_by("name").values_list("name", flat=True).distinct()
    )
    paginator = Paginator(participants, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "users/participants.html",
        {
            "participants": participants,
            "page_obj": page_obj,
            "all_skills": all_skills,
            "active_skill": active_skill,
            "query_prefix": _build_query_prefix(request),
        },
    )


def user_detail_view(request, user_id):
    user = get_object_or_404(User, pk=user_id, is_active=True)
    return render(request, "users/user-details.html", {"user": user})


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(f"/users/{request.user.id}/")
    else:
        form = EditProfileForm(instance=request.user)
    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "user": request.user},
    )


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/users/{request.user.id}/")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {"form": form})


@require_GET
def skills_autocomplete_view(request):
    query = request.GET.get("q", "").strip()
    skills = Skill.objects.filter(name__istartswith=query).order_by("name")[:10]
    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def skill_add_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user.id != user.id:
        return JsonResponse({"error": "forbidden"}, status=403)
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        body = request.POST

    skill = None
    created = False
    added = False

    skill_id = body.get("skill_id")
    name = body.get("name", "").strip()

    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse({"error": "invalid"}, status=400)

    if not user.skills.filter(pk=skill.pk).exists():
        user.skills.add(skill)
        added = True

    return JsonResponse(
        {
            "id": skill.id,
            "name": skill.name,
            "skill_id": skill.id,
            "created": created,
            "added": added,
        }
    )


@login_required
@require_POST
def skill_remove_view(request, user_id, skill_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user.id != user.id:
        return JsonResponse({"error": "forbidden"}, status=403)
    skill = get_object_or_404(Skill, pk=skill_id)
    if user.skills.filter(pk=skill.pk).exists():
        user.skills.remove(skill)
    return JsonResponse({"status": "ok"})
