import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError

PHONE_PATTERN = re.compile(r"^(8\d{10}|\+7\d{10})$")


def validate_phone(phone: str) -> str:
    """Валидатор номера телефона"""
    if not PHONE_PATTERN.match(phone):
        raise ValidationError(
            "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
        )
    return phone


def validate_github_url(url: str) -> str:
    """Валидатор ссылки на GitHub"""
    if not url:
        return url
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValidationError("Ссылка на GitHub должна быть валидной ссылкой")
    host = parsed.netloc.lower().replace("www.", "")
    if host != "github.com":
        raise ValidationError("Ссылка должна вести именно на GitHub")
    return url
