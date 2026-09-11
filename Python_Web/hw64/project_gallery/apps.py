from django.apps import AppConfig


class ProjectGalleryConfig(AppConfig):
    name = 'project_gallery'

    def ready(self):
        import Python_Web.hw64.project_gallery.signals
