from .models import PageView
from django.db.models import F

class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Track views for GET requests that return 200 OK
        if request.method == 'GET' and response.status_code == 200:
            path = request.path
            
            # Exclude admin, media, static files, and favicons to get precise metrics
            if not any(path.startswith(prefix) for prefix in ['/admin/', '/media/', '/static/', '/favicon.ico']):
                try:
                    # Robust atomic tracking: if missing create with 1, otherwise increment atomically
                    obj, created = PageView.objects.get_or_create(path=path, defaults={'views_count': 1})
                    if not created:
                        PageView.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
                except Exception:
                    # Fail silently to avoid interrupting any page loads
                    pass

        return response
