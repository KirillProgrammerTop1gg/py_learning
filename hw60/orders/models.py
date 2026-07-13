from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    PROJECT_TYPES = [
        ('web3_automation', 'Web3 & Crypto Automation'),
        ('backend_dev', 'Python Backend Development'),
        ('frontend_dev', 'Frontend Development (HTML/CSS/JS/React)'),
        ('telegram_bot', 'Telegram Bot / Parser Automation'),
        ('fullstack_dev', 'Fullstack Application'),
        ('other', 'Інше'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Очікує розгляду'),
        ('in_progress', 'В процесі розробки'),
        ('completed', 'Виконано'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Замовник')
    project_name = models.CharField(max_length=150, verbose_name='Назва проекту')
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES, default='other', verbose_name='Тип проекту')
    description = models.TextField(verbose_name='Технічне завдання (опис брифу)')
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бюджет (USD)')
    timeline = models.CharField(max_length=100, verbose_name='Бажані терміни')
    contacts = models.CharField(max_length=200, verbose_name='Контакти для зв\'язку')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка #{self.pk} - {self.project_name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        if not is_new:
            try:
                old_status = Order.objects.get(pk=self.pk).status
            except Order.DoesNotExist:
                pass
                
        super().save(*args, **kwargs)
        
        # Якщо це редагування і статус змінився, відправляємо лист клієнту!
        if not is_new and old_status != self.status:
            self.send_status_update_email(old_status)

    def send_status_update_email(self, old_status):
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.conf import settings
        
        # Перевіряємо наявність email у замовника
        if not self.user.email:
            return
            
        status_colors = {
            'pending': 'Очікує розгляду',
            'in_progress': 'В процесі розробки',
            'completed': 'Виконано',
            'cancelled': 'Скасовано',
        }
        
        current_status_name = status_colors.get(self.status, self.get_status_display())
        old_status_name = status_colors.get(old_status, old_status)
        
        subject = f"Оновлено статус вашого брифу: {self.project_name}"
        domain = getattr(settings, 'SITE_DOMAIN', '127.0.0.1:8000')
        
        # Контекст для HTML-шаблону
        context = {
            'username': self.user.username,
            'project_name': self.project_name,
            'old_status_display': old_status_name,
            'current_status_display': current_status_name,
            'budget': self.budget,
            'timeline': self.timeline,
            'profile_url': f"http://{domain}/orders/profile/",
        }
        
        try:
            # Рендеримо HTML версію
            html_content = render_to_string('emails/client_status_update.html', context)
            
            # Текстова версія листа (якщо поштовий клієнт не підтримує HTML)
            message = f"Вітаємо, @{self.user.username}!\n\n" \
                      f"Статус вашого технічного брифу на розробку проекту \"{self.project_name}\" був змінений розробником в системі!\n\n" \
                      f"--- ЗМІНА СТАТУСУ ---\n" \
                      f"Попередній статус: {old_status_name}\n" \
                      f"Новий статус: {current_status_name}\n\n" \
                      f"--- ДЕТАЛІ ЗАМОВЛЕННЯ ---\n" \
                      f"Назва проекту: {self.project_name}\n" \
                      f"Бюджет: {self.budget} USD\n" \
                      f"Бажані терміни: {self.timeline}\n\n" \
                      f"Ви завжди можете переглянути актуальну історію своїх брифів у вашому особистому кабінеті на сайті.\n" \
                      f"Дякуємо, що обираєте нас!\n\n" \
                      f"З повагою,\n" \
                      f"Розробник Кірілл (Вечірній термінал)"
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[self.user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Помилка відправки листа про зміну статусу клієнту: {e}")


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Клієнт')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review', verbose_name='Заявка (проект)')
    text = models.TextField(verbose_name='Текст відгуку')
    rating = models.IntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Оцінка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']

    def __str__(self):
        return f"Відгук від @{self.user.username} - {self.order.project_name} ({self.rating}/5)"


