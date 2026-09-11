from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = "blog"

    def ready(self):
        import Python_Web.hw66.blog.signals
