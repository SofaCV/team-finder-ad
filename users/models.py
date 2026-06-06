import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator
from django.db import models

from users.avatar import generate_avatar


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if not user.phone:
            user.phone = self._generate_unique_phone()
        if not user.avatar:
            user.avatar = generate_avatar(user.name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("name", "Admin")
        extra_fields.setdefault("surname", "User")
        return self.create_user(email, password, **extra_fields)

    def _generate_unique_phone(self):
        base = 8000000000
        while True:
            phone = f"8{base}"
            if not User.objects.filter(phone=phone).exists():
                return phone
            base += 1


class Skill(models.Model):
    name = models.CharField(max_length=124)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to="avatars/")
    phone = models.CharField(max_length=12)
    github_url = models.URLField(blank=True)
    about = models.CharField(max_length=256, blank=True)
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
