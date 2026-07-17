from django_filters import rest_framework as filters

from .models import Course


class CourseFilter(filters.FilterSet):
    min_students = filters.NumberFilter(
        field_name="students_count", lookup_expr="gte", label="Мінімум студентів"
    )
    max_students = filters.NumberFilter(
        field_name="students_count", lookup_expr="lte", label="Максимум студентів"
    )

    class Meta:
        model = Course
        fields = []
