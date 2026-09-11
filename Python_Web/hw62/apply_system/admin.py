from django.contrib import admin

from .models import Student, Course, Enrollment


class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "age", "created_at")
    list_filter = ("age", "created_at")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("first_name", "last_name")
    readonly_fields = ("created_at",)


class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "duration")
    search_fields = ("title",)
    ordering = ("title",)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "course", "enrollment_date")
    list_filter = ("enrollment_date", "course")
    search_fields = (
        "student__first_name",
        "student__last_name",
        "student__email",
        "course__title",
    )
    autocomplete_fields = ("student", "course")
    readonly_fields = ("enrollment_date",)


admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
