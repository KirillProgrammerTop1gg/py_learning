from django.shortcuts import render
from .models import Article


# Головна сторінка блогу
def home_view(request):
    context = {
        "blog_name": "TechBlog",
        "description": "Найкращі статті про технології та програмування"
    }
    return render(request, "blog/home.html", context)




# Перевірка досвіду користувача (через POST форму)
def check_experience(request):
    experience_years = None
    if request.method == 'POST':
        # Отримуємо число років досвіду з форми, якщо не передано - беремо 0
        experience_years = int(request.POST.get('years', 0))
    return render(request, "blog/experience.html", {"years": experience_years})




# Відображення списку популярних постів
def popular_posts(request):
    posts_data = Article.objects.order_by('-views')[:5]
    
    context = {
        "blog_title": "Популярні статті TechBlog",
        "posts": posts_data,
    }
    return render(request, "blog/popular.html", context)


def about_us(request):
    our_team_data = [
        {
            "name": "Олексій Коваленко", 
            "role": "Засновник & Головний редактор", 
            "email": "alex@techblog.io",
            "bio": "Екс-Senior Python Engineer, фанат чистого коду, системної архітектури та мікросервісів.",
        },
        {
            "name": "Марія Шевченко", 
            "role": "Провідний ШІ Дослідник", 
            "email": "maria.ai@techblog.io",
            "bio": "Досліджує генеративні моделі, LLM та NLP. Вірить, що ШІ та людина - це ідеальний тандем.",
        },
        {
            "name": "Дмитро Петренко", 
            "role": "Frontend Architect", 
            "email": "dima.web@techblog.io",
            "bio": "Створює надшвидкі, доступні та естетичні інтерфейси. Експерт з CSS-magic, UX та Web Performance.",
        }
    ]
    stats_data = [
        {"value": "25,000+", "label": "Читачів щомісяця"},
        {"value": "150+", "label": "Глибоких технічних статей"},
        {"value": "4.9", "label": "Рейтинг матеріалів"}
    ]
    context = {
        "blog_title": "Про нас",
        "description": "Ми - незалежне медіа про розробку програмного забезпечення, штучний інтелект та сучасні технології.",
        "story": "Заснований у 2024 році, TechBlog став затишним простором для розробників будь-якого рівня. Наша мета - створювати контент найвищої якості без зайвої 'води'. Ми пишемо про реальний досвід, ділимося факапами та разом вивчаємо майбутнє.",
        "our_team": our_team_data,
        "stats": stats_data,
    }
    return render(request, "blog/about.html", context)

def contacts(request):
    social_links = [
        {"name": "GitHub", "url": "https://github.com"},
        {"name": "Telegram", "url": "https://t.me"},
        {"name": "LinkedIn", "url": "https://linkedin.com"},
        {"name": "Twitter", "url": "https://twitter.com"},
    ]
    context = {
        "blog_title": "Зв'яжіться з нами",
        "description": "Маєте запитання, пропозицію співпраці чи хочете написати статтю для нас? Залиште повідомлення або зв'яжіться напряму!",
        "blog_email": "hello@techblog.io",
        "blog_phone": "+380 (44) 256-89-90",
        "address": "вул. Хрещатик, 15, Київ, 01001",
        "working_hours": "Понеділок - П'ятниця, 09:00 - 18:00",
        "socials": social_links,
    }
    return render(request, "blog/contact.html", context)