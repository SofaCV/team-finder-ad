# users/managers.py
from django.contrib.auth.models import BaseUserManager

from users.avatar import generate_avatar
from users.constants import PHONE_PREFIX


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
            phone = f"{PHONE_PREFIX}{base}"
            if not self.model.objects.filter(phone=phone).exists():
                return phone
            base += 1
