import json
import os
from django.conf import settings

def developer_profile(request):
    config_path = os.path.join(settings.BASE_DIR, 'portfolio_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {
            "name": "Кирило",
            "role": "Django Backend Developer",
            "greeting": "Привіт!",
            "bio_paragraphs": [],
            "photo_path": "images/avatar.png",
            "contacts": {}
        }
    return {'dev_profile': data}
