from django import forms

from projects.models import Project
from users.validators import validate_github_url


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=[("open", "Открыт"), ("closed", "Закрыт")],
        label="Статус",
    )

    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        labels = {
            "name": "Название проекта",
            "description": "Описание проекта",
            "github_url": "Ссылка на GitHub",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Название проекта обязательно")
        return name

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url", "")
        if url:
            return validate_github_url(url)
        return url
