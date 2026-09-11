import re
from PIL import Image
from django.core.exceptions import ValidationError

def validate_image_security_and_dimensions(file):
    try:
        file.seek(0)
        img = Image.open(file)
        img.verify()
    except Exception:
        raise ValidationError("Завантажений файл не є дійсним зображенням.")

    file.seek(0)
    img = Image.open(file)

    width, height = img.size
    if width < 300 or height < 200:
        raise ValidationError(
            f"Мінімальний дозволений розмір зображення: 300x200px. "
            f"Завантажено: {width}x{height}px."
        )

    try:
        exif = img.getexif() if hasattr(img, 'getexif') else None
        if exif:
            suspicious_patterns = [
                r'<script', r'<\?php', r'eval\(', r'exec\(', r'system\(',
                r'javascript:', r'base64', r'<\?='
            ]
            for tag, value in exif.items():
                val_str = str(value)
                for pattern in suspicious_patterns:
                    if re.search(pattern, val_str, re.IGNORECASE):
                        raise ValidationError("Файл відхилено: виявлено підозрілий контент у метаданих (EXIF).")
    except ValidationError:
        raise
    except Exception:
        pass

    file.seek(0)
