from django import forms
from .models import UserCourse, Course
from django.utils.translation import gettext_lazy as _

from django.forms import modelformset_factory

class CourseForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        label=_("Курс"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    priority = forms.TypedChoiceField(
        coerce=int,
        choices=[("", "---------")] + UserCourse.PRIORITY_CHOICES,
        required=True,
        label=_("Пріоритет"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = UserCourse
        fields = ("course", "priority")


class BaseUserCourseFormSet(forms.BaseModelFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        courses = []
        priorities = []
        has_errors = False

        for form in self.forms:
            # Skip empty forms or forms marked for deletion
            if not form.cleaned_data or (self.can_delete and self._should_delete_form(form)):
                continue

            course = form.cleaned_data.get("course")
            priority = form.cleaned_data.get("priority")

            if course and priority:
                if course in courses:
                    form.add_error("course", _("Ви не можете обрати один і той самий курс кілька разів."))
                    has_errors = True
                else:
                    courses.append(course)

                if priority in priorities:
                    form.add_error("priority", _("Пріоритети вибраних курсів не повинні збігатися."))
                    has_errors = True
                else:
                    priorities.append(priority)

        if has_errors:
            raise forms.ValidationError(_("Будь ласка, виправте помилки у виборі курсів."))


UserCourseFormSet = modelformset_factory(
    UserCourse,
    form=CourseForm,
    formset=BaseUserCourseFormSet,
    extra=3,
    max_num=3,
)