from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва курсу")

    duration = models.PositiveIntegerField(verbose_name="Тривалість (місяців)")

    rating = models.FloatField(
        verbose_name="Оцінка",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        help_text="Оцінка від 0 до 5",
    )

    def __str__(self):
        return f"{self.name} ({self.rating}/5, {self.duration} міс.)"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курси"
        ordering = ["name"]


class UserCourse(models.Model):
    PRIORITY_CHOICES = [
        (1, "Низький"),
        (2, "Середній"),
        (3, "Високий"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="selected_courses",
        verbose_name="Користувач",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="selected_by_users",
        verbose_name="Курс",
    )
    priority = models.PositiveIntegerField(
        choices=PRIORITY_CHOICES, default=2, verbose_name="Пріоритет"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата вибору"
    )

    class Meta:
        verbose_name = "Обраний курс"
        verbose_name_plural = "Обрані курси"
        unique_together = ("user", "course")
        ordering = ["-priority", "course__name"]

    def __str__(self):
        return f"{self.user.username} -> {self.course.name} (Пріоритет: {self.get_priority_display()})"
