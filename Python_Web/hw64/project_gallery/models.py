from django.db import models
from django.conf import settings
from .validators import validate_image_security_and_dimensions

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.title}"


class ProjectGallery(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery_images')
    original_image = models.ImageField(upload_to='gallery/original/', validators=[validate_image_security_and_dimensions])
    thumbnail = models.ImageField(upload_to='gallery/thumbs/', blank=True)
    medium_image = models.ImageField(upload_to='gallery/medium/', blank=True)
    large_image = models.ImageField(upload_to='gallery/large/', blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gallery image for {self.project.title}"