# users/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.avatar import generate_avatar
from users.constants import (
    AVATAR_UPLOAD_PATH,
    SKILL_NAME_MAX_LENGTH,
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)
from users.managers import UserManager


class Skill(models.Model):
    name = models.CharField(max_length=SKILL_NAME_MAX_LENGTH)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # убрали лишний валидатор
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField(max_length=USER_SURNAME_MAX_LENGTH)
    avatar = models.ImageField(upload_to=AVATAR_UPLOAD_PATH)
    phone = models.CharField(max_length=USER_PHONE_MAX_LENGTH)
    github_url = models.URLField(blank=True)
    about = models.CharField(max_length=USER_ABOUT_MAX_LENGTH, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, related_name="users", blank=True)
    favorites = models.ManyToManyField(
        "projects.Project", related_name="interested_users", blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)
