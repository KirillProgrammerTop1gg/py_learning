from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]


class Technology(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        related_name="technologies", 
        verbose_name="Категорія", 
        blank=True, 
        null=True
    )

    def __str__(self):
        if self.category:
            return f"{self.name} ({self.category.name})"
        return self.name

    class Meta:
        verbose_name = "Технологія"
        verbose_name_plural = "Технології"
        ordering = ["category__name", "name"]


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    technologies = models.ManyToManyField(Technology, related_name="projects", verbose_name="Технології")
    date = models.DateField(verbose_name="Дата")
    image = models.ImageField(upload_to="portfolio/projects/", verbose_name="Зображення", blank=True, null=True)
    github_link = models.URLField(verbose_name="GitHub посилання", blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name="Кількість переглядів")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекти"
        ordering = ["-date"]


class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    level = models.PositiveIntegerField(
        verbose_name="Рівень володіння (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=80
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        related_name="skills", 
        verbose_name="Категорія", 
        blank=True, 
        null=True
    )

    def __str__(self):
        if self.category:
            return f"{self.name} ({self.category.name})"
        return self.name

    @property
    def ascii_bar(self):
        filled_length = int(self.level / 5)
        return "#" * filled_length + "-" * (20 - filled_length)

    class Meta:
        verbose_name = "Навичка"
        verbose_name_plural = "Навички"
        ordering = ["category__name", "name"]


class Experience(models.Model):
    position = models.CharField(max_length=100, verbose_name="Посада")
    company = models.CharField(max_length=100, verbose_name="Компанія")
    period = models.CharField(max_length=100, verbose_name="Період")
    description = models.TextField(verbose_name="Опис")
    start_date = models.DateField(verbose_name="Дата початку (для сортування)", blank=True, null=True)

    def __str__(self):
        return f"{self.position} у {self.company}"

    class Meta:
        verbose_name = "Досвід роботи"
        verbose_name_plural = "Досвід роботи"
        ordering = ["-start_date"]


class PageView(models.Model):
    path = models.CharField(max_length=255, unique=True, verbose_name="Шлях сторінки")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Кількість переглядів")
    last_viewed = models.DateTimeField(auto_now=True, verbose_name="Останній перегляд")

    class Meta:
        verbose_name = "Перегляд сторінки"
        verbose_name_plural = "Перегляди сторінок"
        ordering = ["-views_count"]

    def __str__(self):
        return f"{self.path} - {self.views_count}"