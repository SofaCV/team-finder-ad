from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

from users.models import User
from users.validators import validate_github_url, validate_phone


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=124, label="Имя")
    surname = forms.CharField(max_length=124, label="Фамилия")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            self.user = authenticate(username=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Неверный имейл или пароль")
        return cleaned_data


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "avatar": "Аватар",
            "about": "О себе",
            "phone": "Телефон",
            "github_url": "Ссылка на GitHub",
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        try:
            phone = validate_phone(phone)
        except ValidationError as exc:
            raise forms.ValidationError(exc.messages) from exc

        qs = User.objects.filter(phone=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                "Пользователь с таким номером телефона уже существует"
            )
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url", "")
        if url:
            try:
                return validate_github_url(url)
            except forms.ValidationError:
                raise
        return url


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Текущий пароль",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Новый пароль",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтвердите новый пароль",
    )
