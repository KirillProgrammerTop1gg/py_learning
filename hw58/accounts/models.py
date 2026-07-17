from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class User(AbstractUser):
    MIN_AGE = 12
    MAX_AGE = 18
    
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_AGE), MaxValueValidator(MAX_AGE)],
        null=True,
        blank=True,
        verbose_name="Вік",
    )
    phone = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r"^\+380\d{9}$", message="Введіть номер у форматі +380XXXXXXXXX"
            )
        ],
        null=True,
        blank=True,
        verbose_name="Телефон",
    )
    courses = models.ManyToManyField(
        "courses.Course",
        through="courses.UserCourse",
        related_name="users",
        blank=True,
        verbose_name="Курси",
    )
