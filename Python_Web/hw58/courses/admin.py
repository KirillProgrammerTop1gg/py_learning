from django.contrib import admin
from .models import Course, UserCourse


class UserCourseInline(admin.TabularInline):
    model = UserCourse
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "duration", "rating")
    list_filter = ("duration",)
    search_fields = ("name", "rating")
    ordering = ("name",)
    inlines = [UserCourseInline]


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "priority", "created_at")
    list_filter = ("priority", "course", "created_at")
    search_fields = ("user__username", "user__email", "course__name")
    raw_id_fields = ("user", "course")


admin.site.register(Course, CourseAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
