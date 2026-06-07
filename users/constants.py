# constants.py

# Цвета в формате RGB
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_PURPLE = (128, 0, 128)

# Фоновые цвета для аватаров
BACKGROUND_COLORS = [
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_MAGENTA,
    COLOR_YELLOW,
    COLOR_ORANGE,
    COLOR_PURPLE,
    (91, 127, 149),  # серо-голубой
    (120, 144, 156),  # серый
    (96, 125, 139),  # сине-серый
    (117, 117, 117),  # темно-серый
    (109, 125, 136),  # стальной
    (128, 128, 128),  # серый
    (99, 110, 114),  # грифельный
    (112, 128, 144),  # шиферный
    (119, 136, 153),  # светло-шиферный
    (105, 105, 105),  # темно-серый
]

# Константы для настройки аватара
AVATAR_SIZE = 200
AVATAR_FONT_SIZE = 100
AVATAR_TEXT_COLOR = COLOR_WHITE
AVATAR_VERTICAL_OFFSET = 10  # Смещение текста по вертикали для центрирования

# Пути к шрифтам (для разных ОС)
FONT_PATHS = [
    "arial.ttf",  # Windows
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
    "/System/Library/Fonts/Helvetica.ttc",  # macOS
    "/Library/Fonts/Arial.ttf",  # macOS alternative
]

# Длины полей
USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256
SKILL_NAME_MAX_LENGTH = 124

# Телефон
PHONE_PREFIX = "8"

# Аватар
AVATAR_UPLOAD_PATH = "avatars/"

# Пагинация
USERS_PAGE_SIZE = 12

# Автокомплит
SKILLS_AUTOCOMPLETE_LIMIT = 10

# HTTP статусы (дополнительно)
HTTP_403_FORBIDDEN = 403
HTTP_400_BAD_REQUEST = 400