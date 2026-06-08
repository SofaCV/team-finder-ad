# users/utils.py


def normalize_phone(phone: str) -> str:
    """Утилита для нормализации номера телефона (8 -> +7)"""
    phone = phone.strip()
    if phone.startswith("8") and len(phone) == 11:
        return "+7" + phone[1:]
    return phone
