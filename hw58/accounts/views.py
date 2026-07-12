from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ExtendedUserCreationForm
from courses.forms import UserCourseFormSet
from courses.models import UserCourse, Course


def home_view(request):
    courses = Course.objects.all()
    return render(request, "home.html", {"courses": courses})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        course_formset = UserCourseFormSet(
            request.POST,
            queryset=UserCourse.objects.none(),
            prefix="courses"
        )

        if form.is_valid() and course_formset.is_valid():
            user = form.save()

            # Save the selected courses with their priorities for the registered user
            user_courses = course_formset.save(commit=False)
            for user_course in user_courses:
                user_course.user = user
                user_course.save()

            login(request, user)
            return redirect("home")
    else:
        form = ExtendedUserCreationForm()
        course_formset = UserCourseFormSet(
            queryset=UserCourse.objects.none(),
            prefix="courses"
        )

    return render(
        request,
        "accounts/register.html",
        {"form": form, "course_formset": course_formset}
    )


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})


@login_required
def dashboard(request):
    selected_courses = request.user.selected_courses.all()
    return render(
        request,
        "accounts/dashboard.html",
        {"selected_courses": selected_courses}
    )
