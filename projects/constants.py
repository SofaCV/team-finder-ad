# core/constants.py

# Длины полей
PROJECT_NAME_MAX_LENGTH = 200
PROJECT_STATUS_MAX_LENGTH = 6

# Статусы проектов
PROJECT_STATUS_OPEN = "open"
PROJECT_STATUS_CLOSED = "closed"

PROJECT_STATUS_CHOICES = [
    (PROJECT_STATUS_OPEN, "Open"),
    (PROJECT_STATUS_CLOSED, "Closed"),
]

PAGE_SIZE = 12

# HTTP статусы (добавим свои константы для удобства)
HTTP_403_FORBIDDEN = 403
HTTP_400_BAD_REQUEST = 400
