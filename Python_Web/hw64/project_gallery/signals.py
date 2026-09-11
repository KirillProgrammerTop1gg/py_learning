import os
import logging
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import ProjectGallery

logger = logging.getLogger(__name__)

def resize_image(image_field, size):
    image_field.open()
    image_field.seek(0)
    img = Image.open(image_field)
    img = img.convert('RGB')
    
    clean_img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
    
    buffer = BytesIO()
    clean_img.save(buffer, format='JPEG', quality=85)
    
    filename = os.path.basename(image_field.name)
    return ContentFile(buffer.getvalue(), name=filename)

def strip_exif_from_original(image_field):
    image_field.open()
    image_field.seek(0)
    img = Image.open(image_field)
    img = img.convert('RGB')
    
    data = list(img.getdata())
    clean_img = Image.new('RGB', img.size)
    clean_img.putdata(data)
    
    buffer = BytesIO()
    clean_img.save(buffer, format='JPEG', quality=95)
    
    filename = os.path.basename(image_field.name)
    return ContentFile(buffer.getvalue(), name=filename)

@receiver(pre_save, sender=ProjectGallery)
def process_project_gallery_image(sender, instance, **kwargs):
    if not instance.alt_text and instance.project:
        instance.alt_text = f"Зображення для проєкту {instance.project.title}"

    if instance.original_image:
        filename = os.path.basename(instance.original_image.name)
        
        if not getattr(instance, '_exif_stripped', False):
            clean_original = strip_exif_from_original(instance.original_image)
            instance.original_image.save(filename, clean_original, save=False)
            instance._exif_stripped = True
        
        if not instance.thumbnail:
            thumb_file = resize_image(instance.original_image, (150, 150))
            instance.thumbnail.save(f"thumb_{filename}", thumb_file, save=False)
            
        if not instance.medium_image:
            medium_file = resize_image(instance.original_image, (600, 400))
            instance.medium_image.save(f"medium_{filename}", medium_file, save=False)
            
        if not instance.large_image:
            large_file = resize_image(instance.original_image, (1200, 800))
            instance.large_image.save(f"large_{filename}", large_file, save=False)

@receiver(post_save, sender=ProjectGallery)
def log_project_gallery_save(sender, instance, created, **kwargs):
    action = "створено" if created else "оновлено"
    files = []
    if instance.original_image:
        files.append(f"Original: {instance.original_image.name}")
    if instance.thumbnail:
        files.append(f"Thumb: {instance.thumbnail.name}")
    if instance.medium_image:
        files.append(f"Medium: {instance.medium_image.name}")
    if instance.large_image:
        files.append(f"Large: {instance.large_image.name}")

    file_info = ", ".join(files) if files else "немає файлів"
    logger.info(f"[FILE LOG] Галерею (ID: {instance.id}) для проєкту '{instance.project.title}' {action}. Файли: {file_info}")
    print(f"[FILE LOG] Галерею (ID: {instance.id}) для проєкту '{instance.project.title}' {action}. Файли: {file_info}")

    if created:
        User = get_user_model()
        recipients = list(
            User.objects.filter(is_staff=True, is_active=True)
            .exclude(email='')
            .values_list('email', flat=True)
        )

        if not recipients:
            if hasattr(settings, 'ADMINS') and settings.ADMINS:
                recipients = [email for _, email in settings.ADMINS]
            else:
                recipients = ['admin@example.com']

        if recipients:
            subject = f"Нове зображення завантажено: Проєкт '{instance.project.title}'"
            
            try:
                html_message = render_to_string('emails/new_image_notification.html', {
                    'project': instance.project,
                    'image': instance,
                })
                plain_message = strip_tags(html_message)
            except Exception:
                plain_message = f"Нове зображення додано до проєкту {instance.project.title}."
                html_message = None

            try:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
                    recipient_list=recipients,
                    html_message=html_message,
                    fail_silently=False
                )
                logger.info(f"[EMAIL LOG] Повідомлення надіслано на {recipients}")
                print(f"[EMAIL LOG] Повідомлення надіслано на {recipients}")
            except Exception as e:
                logger.error(f"Помилка надсилання e-mail персоналу: {e}")
                print(f"Помилка надсилання e-mail персоналу: {e}")



@receiver(post_delete, sender=ProjectGallery)
def log_project_gallery_delete(sender, instance, **kwargs):
    logger.info(f"[FILE LOG] Галерею (ID: {instance.id}) для проєкту '{instance.project.title}' було видалено.")
    print(f"[FILE LOG] Галерею (ID: {instance.id}) для проєкту '{instance.project.title}' було видалено.")

