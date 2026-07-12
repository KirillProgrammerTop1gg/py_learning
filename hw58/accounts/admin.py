from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from courses.models import UserCourse


class UserCourseInline(admin.TabularInline):
    model = UserCourse
    extra = 1


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age", "phone")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("age", "phone")}),)
    inlines = [UserCourseInline]


admin.site.register(User, CustomUserAdmin)
