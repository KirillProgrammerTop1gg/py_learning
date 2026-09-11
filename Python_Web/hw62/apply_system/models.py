from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)


class Student(models.Model):
    MIN_AGE = 16
    MAX_AGE = 25

    first_name = models.CharField(
        max_length=50, validators=[MinLengthValidator(2)], verbose_name="Ім'я"
    )
    last_name = models.CharField(
        max_length=50, validators=[MinLengthValidator(2)], verbose_name="Прізвище"
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_AGE), MaxValueValidator(MAX_AGE)],
        null=True,
        blank=True,
        verbose_name="Вік",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    title = models.CharField(
        unique=True,
        max_length=100,
        validators=[MinLengthValidator(5)],
        verbose_name="Назва",
    )
    description = models.TextField(
        unique=True, validators=[MinLengthValidator(5)], verbose_name="Опис"
    )
    duration = models.PositiveIntegerField(
        validators=[MaxValueValidator(1000)], verbose_name="Тривалість (години)"
    )

    students = models.ManyToManyField(
        Student, through="Enrollment", related_name="courses"
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")
