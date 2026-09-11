import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()

NAME_REGEX = re.compile(r"^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ'\s-]+$")


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Електронна пошта"),
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "example@email.com"}
        ),
    )

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label=_("Ім'я"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Введіть ваше ім'я")}
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        label=_("Прізвище"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Введіть ваше прізвище")}
        ),
    )

    age = forms.IntegerField(
        min_value=User.MIN_AGE,
        max_value=User.MAX_AGE,
        required=True,
        label=_("Вік"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Введіть ваш вік"),
                "min": User.MIN_AGE,
                "max": User.MAX_AGE,
            }
        ),
    )

    phone = forms.CharField(
        required=False,
        label=_("Телефон"),
        widget=forms.TelInput(
            attrs={"class": "form-control", "placeholder": "+380501234567"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "age",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Налаштування віджетів для полів з базової форми
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": _("Введіть логін")}
        )
        if "password1" in self.fields:
            self.fields["password1"].widget.attrs.update(
                {"class": "form-control", "placeholder": _("Введіть пароль")}
            )
        if "password2" in self.fields:
            self.fields["password2"].widget.attrs.update(
                {"class": "form-control", "placeholder": _("Підтвердіть пароль")}
            )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return email

        # Нормалізуємо email
        email = email.strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Користувач з таким email вже існує!"))

        if email.endswith("@test.com"):
            raise forms.ValidationError(_("Тестові email адреси заборонені"))

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            return phone

        # Покращуємо UX: видаляємо пробіли, дужки, дефіси
        cleaned_phone = re.sub(r"[\s\-\(\)]", "", phone)

        # Валідуємо фінальний формат
        if not re.match(r"^\+380\d{9}$", cleaned_phone):
            raise forms.ValidationError(_("Введіть номер у форматі +380XXXXXXXXX"))

        if User.objects.filter(phone=cleaned_phone).exists():
            raise forms.ValidationError(_("Користувач з таким телефоном вже існує!"))

        return cleaned_phone

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip()
        if not first_name:
            raise forms.ValidationError(_("Це поле є обов'язковим."))

        if not NAME_REGEX.match(first_name):
            raise forms.ValidationError(
                _("Ім'я має містити тільки букви, дефіси або апострофи")
            )

        if len(first_name) < 2:
            raise forms.ValidationError(_("Ім'я має містити мінімум 2 символи"))

        return first_name.title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "").strip()
        if not last_name:
            raise forms.ValidationError(_("Це поле є обов'язковим."))

        if not NAME_REGEX.match(last_name):
            raise forms.ValidationError(
                _("Прізвище має містити тільки букви, дефіси або апострофи")
            )

        if len(last_name) < 2:
            raise forms.ValidationError(_("Прізвище має містити мінімум 2 символи"))

        return last_name.title()

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        username = cleaned_data.get("username")

        if first_name and username and first_name.lower() == username.lower():
            raise forms.ValidationError(_("Логін не може співпадати з ім'ям"))

        return cleaned_data
