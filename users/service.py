# users/service.py
from django.core.paginator import Paginator

from users.constants import USERS_PAGE_SIZE


def build_query_prefix(request, exclude=None):
    """Построение префикса для сохранения параметров запроса"""
    params = []
    for key, value in request.GET.items():
        if key == "page" or key in (exclude or []):
            continue
        params.append(f"{key}={value}")
    return "&".join(params) + ("&" if params else "")


def paginate_queryset(queryset, request, page_size=USERS_PAGE_SIZE):
    """Универсальная функция для пагинации"""
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(request.GET.get("page"))
    query_prefix = build_query_prefix(request)
    return page_obj, query_prefix
