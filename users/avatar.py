import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

BACKGROUND_COLORS = [
    (91, 127, 149),
    (120, 144, 156),
    (96, 125, 139),
    (117, 117, 117),
    (109, 125, 136),
    (128, 128, 128),
    (99, 110, 114),
    (112, 128, 144),
    (119, 136, 153),
    (105, 105, 105),
]


def generate_avatar(name: str) -> ContentFile:
    letter = name[0].upper() if name else "?"
    color = random.choice(BACKGROUND_COLORS)
    size = 200
    image = Image.new("RGB", (size, size), color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) / 2, (size - text_height) / 2 - 10)
    draw.text(position, letter, fill=(255, 255, 255), font=font)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"avatar_{letter}.png")
