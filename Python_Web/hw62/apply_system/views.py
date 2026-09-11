from django.db.models import Count

from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Student, Course, Enrollment
from .serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer
from .permissions import IsStaffOrReadOnly
from .filters import CourseFilter


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by("id")
    serializer_class = StudentSerializer
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "email"]
    throttle_scope = "students"


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.annotate(
        students_count=Count("students")
    ).prefetch_related("students").order_by("id")
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    permission_classes = [IsStaffOrReadOnly]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'course').order_by("id")
    serializer_class = EnrollmentSerializer
