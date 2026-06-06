import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError

PHONE_PATTERN = re.compile(r"^(8\d{10}|\+7\d{10})$")


def normalize_phone(phone: str) -> str:
    phone = phone.strip()
    if phone.startswith("8") and len(phone) == 11:
        return "+7" + phone[1:]
    return phone


def validate_phone(phone: str) -> str:
    if not PHONE_PATTERN.match(phone):
        raise ValidationError(
            "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
        )
    return normalize_phone(phone)


def validate_github_url(url: str) -> str:
    if not url:
        return url
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValidationError("Ссылка на GitHub должна быть валидной ссылкой")
    host = parsed.netloc.lower().replace("www.", "")
    if host != "github.com":
        raise ValidationError("Ссылка должна вести именно на GitHub")
    return url
