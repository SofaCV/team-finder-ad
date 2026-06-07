import io
import random
import warnings

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from .constants import (
    AVATAR_SIZE,
    AVATAR_FONT_SIZE,
    AVATAR_TEXT_COLOR,
    AVATAR_VERTICAL_OFFSET,
    BACKGROUND_COLORS,
    FONT_PATHS,
)


def calculate_text_position(
    image_size: int, text_bbox: tuple, vertical_offset: int = 0
) -> tuple:
    """
    Рассчитывает позицию для центрирования текста на изображении.

    Args:
        image_size: Размер изображения (ширина и высота)
        text_bbox: Bounding box текста в формате (left, top, right, bottom)
        vertical_offset: Дополнительное вертикальное смещение

    Returns:
        tuple: (x, y) координаты для размещения текста
    """
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (image_size - text_width) // 2
    y = (image_size - text_height) // 2 - vertical_offset

    return x, y


def get_font(font_size: int):
    """
    Возвращает шрифт указанного размера.
    Перебирает список возможных путей к шрифтам.
    """
    # Пробуем загрузить шрифт из списка путей
    for font_path in FONT_PATHS:
        try:
            return ImageFont.truetype(font_path, font_size)
        except (OSError, IOError):
            continue

    warnings.warn(
        f"No TrueType fonts found. Using default font which may be too small. "
        f"Requested size: {font_size}px"
    )
    return ImageFont.load_default()


def generate_avatar(
    name: str, size: int = AVATAR_SIZE, font_size: int = AVATAR_FONT_SIZE
) -> ContentFile:
    """
    Генерирует аватар на основе имени пользователя.

    Args:
        name: Имя пользователя
        size: Размер аватара в пикселях (по умолчанию AVATAR_SIZE)
        font_size: Размер шрифта (по умолчанию AVATAR_FONT_SIZE)

    Returns:
        ContentFile: Файл с изображением аватара
    """
    letter = name[0].upper() if name else "?"
    background_color = random.choice(BACKGROUND_COLORS)

    image = Image.new("RGB", (size, size), background_color)
    draw = ImageDraw.Draw(image)

    font = get_font(font_size)

    bbox = draw.textbbox((0, 0), letter, font=font)
    position = calculate_text_position(size, bbox, AVATAR_VERTICAL_OFFSET)

    draw.text(position, letter, fill=AVATAR_TEXT_COLOR, font=font)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return ContentFile(buffer.read(), name=f"avatar_{letter}_{size}x{size}.png")
