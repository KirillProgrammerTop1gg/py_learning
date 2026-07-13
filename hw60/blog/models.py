from django.db import models
from django.contrib.auth import get_user_model
from portfolio.models import Category, Technology

User = get_user_model()

def transliterate_slug(string):
    # Ukrainian translit dictionary for Cyrillic slugify
    ukr_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'yu', 'я': 'ya', ' ': '-', '-': '-', '.': '', ',': '', '_': '-', ':': '', ';': '',
        '\\': '', '/': '', '"': '', '\'': '', '`': ''
    }
    res = []
    for char in string.lower():
        if char in ukr_map:
            res.append(ukr_map[char])
        elif char.isalnum():
            res.append(char)
    slug = "".join(res)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-')[:150]


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Слаг (URL)", blank=True)
    content = models.TextField(verbose_name="Вміст статті")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
        verbose_name="Категорія"
    )
    technologies = models.ManyToManyField(
        Technology,
        blank=True,
        related_name="blog_posts",
        verbose_name="Технології"
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name="Кількість переглядів")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        verbose_name = "Стаття блогу"
        verbose_name_plural = "Статті блогу"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliterate_slug(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments", verbose_name="Стаття")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name="Автор")
    text = models.TextField(verbose_name="Текст коментаря")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ["created_at"]  # Chronological order for comment rendering

    def __str__(self):
        return f"Коментар від @{self.user.username} до {self.post.title}"
