import json
from http import HTTPStatus

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from users.constants import SKILLS_AUTOCOMPLETE_LIMIT, USERS_PAGE_SIZE
from users.forms import (
    EditProfileForm,
    LoginForm,
    PasswordChangeForm,
    RegistrationForm,
)
from users.models import Skill, User
from core.service import paginate_queryset


def register_view(request):
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            name=form.cleaned_data["name"],
            surname=form.cleaned_data["surname"],
        )
        login(request, user)
        return redirect(reverse("projects:project_list"))

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        login(request, form.user)
        return redirect(reverse("projects:project_list"))

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(reverse("projects:project_list"))


def participants_list_view(request):
    participants = User.objects.filter(is_active=True).order_by("-id")
    active_skill = request.GET.get("skill", "")

    if active_skill:
        participants = participants.filter(skills__name=active_skill).distinct()

    all_skills = (
        Skill.objects.order_by("name").values_list("name",
                                                   flat=True).distinct()
    )

    page_obj, query_prefix = paginate_queryset(participants, request,
                                               USERS_PAGE_SIZE)

    return render(
        request,
        "users/participants.html",
        {
            "participants": participants,
            "page_obj": page_obj,
            "all_skills": all_skills,
            "active_skill": active_skill,
            "query_prefix": query_prefix,
        },
    )


def user_detail_view(request, user_id):
    user = get_object_or_404(User, pk=user_id, is_active=True)
    return render(request, "users/user-details.html", {"user": user})


@login_required
def edit_profile_view(request):
    form = EditProfileForm(
        request.POST or None, request.FILES or None, instance=request.user
    )

    if form.is_valid():
        form.save()
        return redirect(reverse("users:user_detail", args=[request.user.id]))

    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "user": request.user},
    )


@login_required
def change_password_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(reverse("users:user_detail", args=[request.user.id]))

    return render(request, "users/change_password.html", {"form": form})


@require_GET
def skills_autocomplete_view(request):
    query = request.GET.get("q", "").strip()
    skills = Skill.objects.filter(name__istartswith=query).order_by("name")[
        :SKILLS_AUTOCOMPLETE_LIMIT
    ]
    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def skill_add_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.id != user.id:
        return JsonResponse({"error": "forbidden"},
                            status=HTTPStatus.FORBIDDEN)

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
        return JsonResponse({"error": "invalid"},
                            status=HTTPStatus.BAD_REQUEST)

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
        return JsonResponse({"error": "forbidden"},
                            status=HTTPStatus.FORBIDDEN)

    skill = get_object_or_404(Skill, pk=skill_id)

    if user.skills.filter(pk=skill.pk).exists():
        user.skills.remove(skill)

    return JsonResponse({"status": "ok"})
