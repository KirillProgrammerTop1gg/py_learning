import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from Python_Web.hw64.project_gallery.models import Project, ProjectGallery

User = get_user_model()

def generate_sample_image(title, subtitle, bg_color, text_color, size=(1200, 900)):
    image = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(image)

    # Draw decorative geometric elements
    draw.rectangle([40, 40, size[0] - 40, size[1] - 40], outline=text_color, width=5)
    draw.ellipse([size[0] - 300, 50, size[0] - 100, 250], fill=(255, 255, 255, 30))
    draw.polygon([(100, size[1] - 100), (250, size[1] - 300), (400, size[1] - 100)], fill=(255, 255, 255, 40))

    # Add text banner
    draw.text((100, size[1] // 2 - 60), title, fill=text_color)
    draw.text((100, size[1] // 2 + 20), subtitle, fill=text_color)

    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=90)
    buffer.seek(0)
    return buffer.getvalue()

class Command(BaseCommand):
    help = "Seeds database with test projects and generated images"

    def handle(self, *args, **options):
        self.stdout.write("Seeding test projects and images...")

        # 1. Create or get admin user
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True
            }
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))

        # 2. Project data
        projects_data = [
            {
                "title": "Сучасна Вілла 'Horizon'",
                "description": "Концептуальний проєкт житлової вілли з панорамним заскленням та терасою.",
                "images": [
                    ("Horizon Exterior", "Фасад та головний вхід", (41, 128, 185), (255, 255, 255)),
                    ("Horizon Living Room", "Інтер'єр вітальні з каміном", (39, 174, 96), (255, 255, 255)),
                    ("Horizon Pool Deck", "Басейн та зона відпочинку", (142, 68, 173), (255, 255, 255)),
                ]
            },
            {
                "title": "Smart Eco Home",
                "description": "Автономний заміський будинок з сонячними панелями та системою розумного дому.",
                "images": [
                    ("Solar Panels System", "Дахові сонячні панелі 15kW", (211, 84, 0), (255, 255, 255)),
                    ("Smart Control Panel", "Центральна панель керування", (44, 62, 80), (255, 255, 255)),
                ]
            },
            {
                "title": "FinTech Mobile App",
                "description": "Дизайн UI/UX мобільного застосунку для онлайн-банкінгу та криптогаманця.",
                "images": [
                    ("Dashboard UI", "Головний екран балансу та аналітики", (52, 73, 94), (255, 255, 255)),
                    ("Transaction Flow", "Екран швидкого переказу коштів", (22, 160, 133), (255, 255, 255)),
                ]
            }
        ]

        # 3. Create projects & images
        for p_info in projects_data:
            project, p_created = Project.objects.get_or_create(
                title=p_info["title"],
                defaults={
                    "description": p_info["description"],
                }
            )

            if p_created:
                self.stdout.write(f"Created project: {project.title}")
            else:
                self.stdout.write(f"Project already exists: {project.title}")

            for idx, (img_title, img_sub, bg_col, text_col) in enumerate(p_info["images"], 1):
                img_bytes = generate_sample_image(img_title, img_sub, bg_col, text_col)
                filename = f"sample_{project.id}_{idx}.jpg"

                gallery_item = ProjectGallery.objects.create(
                    project=project,
                    original_image=ContentFile(img_bytes, name=filename)
                )
                self.stdout.write(
                    f"  - Added image #{gallery_item.id}: {filename} (Thumb: {gallery_item.thumbnail.name})"
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded test projects and images!"))
