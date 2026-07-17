from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("students", views.StudentViewSet)
router.register("courses", views.CourseViewSet)
router.register("enrollments", views.EnrollmentViewSet)

urlpatterns = router.urls
