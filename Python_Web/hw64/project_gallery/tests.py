import os
import shutil
import tempfile
from io import BytesIO
from PIL import Image
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.core import mail
from django.contrib.auth import get_user_model

from .models import Project, ProjectGallery
from .validators import validate_image_security_and_dimensions

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp()

def create_test_image(size=(800, 600), format='JPEG', exif_data=None):
    img = Image.new('RGB', size, color=(73, 109, 137))
    buffer = BytesIO()
    if exif_data:
        exif = img.getexif()
        exif[270] = exif_data
        img.save(buffer, format=format, exif=exif)
    else:
        img.save(buffer, format=format)
    buffer.seek(0)
    return SimpleUploadedFile("test_image.jpg", buffer.getvalue(), content_type="image/jpeg")

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ProjectGalleryTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staff_member',
            email='staff@example.com',
            password='password',
            is_staff=True,
            is_active=True
        )
        self.project = Project.objects.create(
            title="Тестовий Проєкт",
            description="Опис тестового проєкту"
        )

    def test_validator_valid_image(self):
        valid_file = create_test_image((400, 300))
        try:
            validate_image_security_and_dimensions(valid_file)
        except ValidationError:
            self.fail("validate_image_security_and_dimensions raised ValidationError unexpectedly!")

    def test_validator_small_image(self):
        small_file = create_test_image((200, 150))
        with self.assertRaises(ValidationError) as ctx:
            validate_image_security_and_dimensions(small_file)
        self.assertIn("Мінімальний дозволений розмір", str(ctx.exception))

    def test_validator_invalid_file(self):
        invalid_file = SimpleUploadedFile("fake.jpg", b"not an image", content_type="image/jpeg")
        with self.assertRaises(ValidationError) as ctx:
            validate_image_security_and_dimensions(invalid_file)
        self.assertIn("не є дійсним зображенням", str(ctx.exception))

    def test_validator_malicious_exif(self):
        malicious_file = create_test_image((400, 300), exif_data="<script>alert('xss')</script>")
        with self.assertRaises(ValidationError) as ctx:
            validate_image_security_and_dimensions(malicious_file)
        self.assertIn("виявлено підозрілий контент", str(ctx.exception))

    def test_gallery_image_creation_resizes_alt_text_and_staff_email(self):
        uploaded_file = create_test_image((1000, 800))
        gallery_item = ProjectGallery.objects.create(
            project=self.project,
            original_image=uploaded_file
        )

        # 1. Alt-text generated automatically
        self.assertEqual(gallery_item.alt_text, f"Зображення для проєкту {self.project.title}")

        # 2. Resized images created
        self.assertTrue(gallery_item.thumbnail)
        self.assertTrue(gallery_item.medium_image)
        self.assertTrue(gallery_item.large_image)

        # Verify sizes
        thumb_img = Image.open(gallery_item.thumbnail.path)
        self.assertEqual(thumb_img.size, (150, 150))

        medium_img = Image.open(gallery_item.medium_image.path)
        self.assertEqual(medium_img.size, (600, 400))

        large_img = Image.open(gallery_item.large_image.path)
        self.assertEqual(large_img.size, (1200, 800))

        # 3. Email sent to staff user
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['staff@example.com'])
        self.assertIn(self.project.title, mail.outbox[0].subject)

    def test_exif_stripping(self):
        file_with_exif = create_test_image((500, 400), exif_data="Normal metadata info")
        gallery_item = ProjectGallery.objects.create(
            project=self.project,
            original_image=file_with_exif
        )

        saved_img = Image.open(gallery_item.original_image.path)
        exif = saved_img.getexif()
        # EXIF should be empty after stripping
        self.assertEqual(len(exif), 0)