from django.contrib import admin
from .models import Project, ProjectGallery

class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = [ProjectGalleryInline]

class ProjectGalleryAdmin(admin.ModelAdmin):
    list_display = ('project', 'uploaded_at')

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectGallery, ProjectGalleryAdmin)
