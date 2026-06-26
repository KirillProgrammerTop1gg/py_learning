from django.shortcuts import render
from datetime import date

def home_view(request):
    # Короткі відомості про розробника
    bio_data = {
        "name": "Кірілл",
        "age": 15,
        "experience": "Кілька років тому я захопився світом програмування та технологій. З того часу я щодня вивчаю нові інструменти, створюю веб-додатки та розробляю корисних Telegram-ботів.",
        "location": "Київ, Україна",
        "role": "Python & Frontend Developer"
    }
    
    # Структуровані навички з піднавичками та прогресом
    skills_data = [
        {
            "category": "Frontend Розробка",
            "overall_progress": 100,
            "description": "Повний цикл створення клієнтської частини: від семантичної верстки до інтерактивної логіки.",
            "subskills": [
                {"name": "HTML5 & Semantic Markup", "progress": 100},
                {"name": "CSS3 & Modern Layouts (Grid/Flexbox/Variables)", "progress": 100},
                {"name": "JavaScript (ES6+ & Async/Await)", "progress": 100},
                {"name": "Responsive & Mobile-First Design", "progress": 100}
            ]
        },
        {
            "category": "Python Розробка",
            "overall_progress": 50,
            "description": "Створення серверної логіки, робота з веб-фреймворками та розробка асинхронних ботів.",
            "subskills": [
                {"name": "Python Core (ООП, структури даних, декоратори, винятки)", "progress": 100},
                {"name": "Web-Frameworks (Flask, FastAPI, 60% Django)", "progress": 60},
                {"name": "Data Science & Database Work (SQLAlchemy, Pandas, NumPy)", "progress": 0}
            ]
        }
    ]
    
    # Список розроблених проєктів
    projects_data = [
        {
            "title": "Ресторан на Flask",
            "tech_stack": "Python, Flask, Jinja2, CSS Grid",
            "description": "Сучасна веб-платформа для замовлення страв у ресторані з інтерактивним меню, кошиком покупця та адмін-панеллю для перегляду нових замовлень.",
            "category": "Web App",
            "emoji": "🍔",
            "created_at": date(2024, 5, 12)
        },
        {
            "title": "Сервіс для ремонту",
            "tech_stack": "Python, Django, PostgreSQL, JavaScript",
            "description": "Повноцінний веб-сервіс для автоматизації сервісних центрів. Дозволяє вести облік заявок, контролювати етапи ремонту та вести клієнтську базу.",
            "category": "Web App",
            "emoji": "🔧",
            "created_at": date(2024, 11, 20)
        },
        {
            "title": "Telegram-бот для сервісу ремонту",
            "tech_stack": "FastAPI, aiogram, REST API, Webhooks",
            "description": "Чат-бот, інтегрований із сервісом ремонту через FastAPI. Надає користувачам можливість миттєво перевіряти статус замовлення за його номером.",
            "category": "Telegram Bot",
            "emoji": "🤖",
            "created_at": date(2025, 1, 15)
        },
        {
            "title": "Бот для синхронного відкриття угод",
            "tech_stack": "Python, aiogram, Asyncio, API Біржі",
            "description": "Спеціалізований асинхронний бот для копіювання торгових операцій. Дозволяє синхронно відкривати та управляти угодами на кількох акаунтах у Telegram.",
            "category": "FinTech Bot",
            "emoji": "📈",
            "created_at": date(2025, 4, 10)
        }
    ]
    
    context = {
        "bio": bio_data,
        "skills": skills_data,
        "projects": projects_data,
        "blog_title": "Мій кабінет розробника"
    }
    return render(request, "portfolio/home.html", context)