# 🐍 Python Learning Repository

This repository contains my Python backend learning projects built with **Flask**, **FastAPI**, and **Django**.
It covers real-world tasks such as:

- 🌐 Web development
- 🕷 Web scraping
- 🗄 Database integration
- 🔐 Authentication systems
- ⚡ REST APIs

---

## 📂 Projects

<details>
<summary>🔹 <b>hw_16 — Brocard Scraper & Shop Clone</b></summary>
Flask application that scrapes perfume data from the **Brocard** website and displays it as an online shop.
### 🚀 Features
- Website scraping
- Product catalog
- Order page
- Database integration
### 🛠 Libraries
`flask`, `sqlalchemy`, `requests`, `parser`
</details>
---
<details>
<summary>🔹 <b>hw_18 — QR & AI HTML Generator</b></summary>
Web app for generating **QR codes** and AI-generated HTML pages.
### 🚀 Features
- QR code generation
- AI-based HTML generation
### 🛠 Libraries
`flask`, `google-genai`
</details>
---
<details>
<summary>🔹 <b>hw_20 — Shop Clone with Admin Panel</b></summary>
Extended version of the shop with admin functionality.
### 🚀 Features
- Admin authentication
- Product & image management
- Custom 404 page
- Database integration
### 🛠 Libraries
`flask`, `sqlalchemy`, `requests`, `parser`
</details>
---
<details>
<summary>🔹 <b>hw_22 — Сфера: Social Messenger</b></summary>
Flask-based social network with messaging system.
### 🚀 Features
- Authentication (Flask-Login)
- Friend system
- Private messaging
- CSRF protection
- Responsive UI
### 🛠 Libraries
`flask`, `flask-login`, `flask-wtf`, `wtforms`, `sqlalchemy`
</details>
---
<details>
<summary>🔹 <b>hw_24 — Flask Logging & Testing</b></summary>
Microservices demonstrating logging and testing.
### 🚀 Features
- Logging system
- JSON API
- Request validation
- Unit testing
### 🛠 Libraries
`flask`, `logging`, `unittest`
</details>
---
<details>
<summary>🔹 <b>hw_32 — FastAPI User Manager</b></summary>
REST API for managing users.
### 🚀 Features
- Add / delete users
- Duplicate validation
- Error handling
- HTTP status codes
### 🛠 Libraries
`fastapi`, `uvicorn`
</details>
---
<details>
<summary>🔹 <b>hw_34 — FastAPI Task Manager</b></summary>
Full CRUD API with validation and testing.
### 🚀 Features
- Create / update / delete tasks
- UUID-based operations
- Validation via Pydantic
- Automated tests
### 🛠 Libraries
`fastapi`, `uvicorn`, `pydantic`, `pytest`
</details>
---
<details>
<summary>🔹 <b>hw_36 — FastAPI Event Participants</b></summary>
Async REST API for managing event participants with PostgreSQL.
### 🚀 Features
- Add participants with full validation
- Fetch participants by event name
- Unique email enforcement
- Async SQLAlchemy + asyncpg
- Load testing (sync vs async comparison)
### 📡 Endpoints
- `POST /participants/` — Register a new participant
- `GET /participants/event/{event_name}` — List participants of a specific event
### ✅ Validation
- `email` — must be a valid email address
- `name` — must not contain digits
- `age` — must be between 12 and 120
- `email` — must be unique in the database (409 on conflict)
### 🛠 Libraries
`fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `asyncpg`, `aiohttp`
</details>
---
<details>
<summary>🔹 <b>hw_38 — FastAPI Animals API with Alembic Migrations</b></summary>
Versioned async REST API for managing shelter animals, with PostgreSQL and Alembic schema migrations.
### 🚀 Features
- Versioned API (v1 / v2) with separate schemas and routers
- Full error handling: HTTP 400, 404, 422 with descriptive messages
- Schema migrations via **Alembic** (async engine)
- `health_status` field added through a real migration (not `create_all`)
- Task endpoint with out-of-range validation and console logging
### 📡 Endpoints
**v1** — fields: `id`, `name`, `age`, `adopted`
- `POST /v1/animals/` — Create a new animal
- `GET /v1/animals/{animal_id}` — Get animal by ID

**v2** — fields: `id`, `name`, `age`, `adopted`, `health_status`

- `POST /v2/animals/` — Create a new animal with health status
- `GET /v2/animals/{animal_id}` — Get animal by ID including health status

**tasks**

- `GET /tasks/{task_id}` — Get task by ID

### ✅ Validation & Error Handling

- `age <= 0` — HTTP **400** Bad Request
- animal / task not found — HTTP **404** Not Found
- `task_id > 1000` — HTTP **422** Unprocessable Entity with custom message
- `name` — must not contain digits
- `health_status` — must be `"healthy"` or `"sick"` (v2 only)
- All errors logged to console via `logging`

### 🗄 Migrations

Two Alembic migrations in sequence:

1. `2bbd53f56901` — `init` (initial table structure: `id`, `name`, `age`, `adopted`)
2. `612345b16570` — `add_health_status_to_animal` (adds `health_status` column with `server_default="healthy"`)

### 🛠 Libraries

`fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `asyncpg`, `alembic`
</details>
---
<details>
<summary>🔹 <b>hw_40 — SkillSwap API</b></summary>

Async REST API платформи для обміну навичками між користувачами з JWT-автентифікацією та розширеною статистикою.

### 🚀 Features

- Повний CRUD для користувачів, навичок, категорій, обмінів і відгуків
- JWT-автентифікація через Bearer-токен (`PyJWT`)
- Перевірка прав доступу на рівні роутів (власник / адмін)
- Система обміну навичками зі статусами: `pending → accepted → completed`
- Відгуки тільки після завершеного обміну, без дублікатів
- Пошук навичок за назвою/описом, фільтрація за категорією
- Статистика: топ навичок, найактивніші юзери, success rate обмінів
- Async SQLAlchemy + asyncpg, `selectinload` для eager loading зв'язків

### 📡 Endpoints

**auth**

- `POST /token` — Отримати JWT-токен за username

**users**

- `POST /api/users/` — Реєстрація користувача
- `GET /api/users/` — Список користувачів
- `GET /api/users/me` — Власний профіль (🔒)
- `GET /api/users/{user_id}` — Профіль користувача
- `PUT /api/users/me` — Оновити власний профіль (🔒)
- `PUT /api/users/{user_id}` — Оновити профіль (🔒 власник або адмін)
- `GET /api/users/{user_id}/skills` — Навички користувача

**categories**

- `GET /api/categories/` — Список категорій (з кількістю навичок)
- `GET /api/categories/{id}` — Категорія за ID
- `GET /api/categories/slug/{slug}` — Категорія за slug
- `GET /api/categories/{id}/skills` — Категорія з усіма навичками
- `POST /api/categories/` — Створити категорію (🔒)
- `PUT /api/categories/{id}` — Оновити категорію (🔒)
- `DELETE /api/categories/{id}` — Видалити категорію (🔒, неможливо якщо є навички)

**skills**

- `GET /api/skills/` — Список навичок (фільтри: `category_id`, `can_teach`, `want_learn`, `search`)
- `GET /api/skills/{id}` — Навичка за ID
- `POST /api/skills/` — Створити навичку (🔒)
- `PUT /api/skills/{id}` — Оновити навичку (🔒)
- `DELETE /api/skills/{id}` — Видалити навичку (🔒)
- `GET /api/skills/{id}/matches` — Знайти збіги для обміну

**exchanges**

- `GET /api/exchanges/` — Список обмінів (фільтри: `status`, `user_id`, `from_date`, `to_date`, `sort_order`)
- `GET /api/exchanges/my/sent` — Надіслані запити (🔒)
- `GET /api/exchanges/my/received` — Отримані запити (🔒)
- `GET /api/exchanges/{id}` — Деталі обміну (🔒)
- `POST /api/exchanges/` — Створити запит на обмін (🔒)
- `PUT /api/exchanges/{id}` — Змінити статус обміну (🔒)

**reviews**

- `GET /api/reviews/` — Список відгуків
- `GET /api/reviews/{id}` — Відгук за ID
- `GET /api/reviews/user/{user_id}` — Відгуки про користувача
- `GET /api/reviews/user/{user_id}/rating` — Середній рейтинг користувача
- `POST /api/reviews/` — Залишити відгук (🔒, тільки після completed обміну)

**stats**

- `GET /api/stats/top-skills` — Топ навичок за кількістю користувачів
- `GET /api/stats/active-users` — Найактивніші користувачі
- `GET /api/stats/exchange-success-rate` — Статистика успішності обмінів

### ✅ Validation & Business Logic

- `can_teach` та `want_learn` не можуть бути `true` одночасно для однієї навички
- Обмін з самим собою заборонено (HTTP **400**)
- Прийняти/відхилити обмін може лише отримувач, скасувати — будь-який учасник
- Відгук можна залишити лише якщо обмін має статус `completed` (HTTP **400** інакше)
- Повторний відгук на один обмін від одного юзера заборонено
- Видалення категорії з прив'язаними навичками → HTTP **409 Conflict**
- Slug категорії валідується регулярним виразом: `^[a-z0-9]+(?:-[a-z0-9]+)*$`

### 🔐 Authentication

JWT-токен у заголовку `Authorization: Bearer <token>`. Токен містить `user_id` та `role`.  
Для тестування: `POST /token` з `{"user_id": 1, "role": "user"}`.

### 🗄 Models

`User` ↔ `Skill` (many-to-many через `skill_user_association`)  
`Skill` → `Category` (many-to-one)  
`Exchange` → `User` (sender + receiver), `Skill`  
`Review` → `Exchange`, `User` (reviewer + reviewed)

### 🛠 Libraries

`fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `asyncpg`, `PyJWT`, `python-dotenv`

</details>
---
<details>
<summary>🔹 <b>hw_42 — FastAPI Photo Storage</b></summary>

Async REST API for uploading and serving images with file validation.

### 🚀 Features

- Secure file upload with MIME-type validation
- Streaming upload (chunk-by-chunk, no memory overload)
- PIL-based image integrity verification
- Path traversal protection
- Unique filename generation with sanitization
- Sorted photo listing by upload date

### 📡 Endpoints

- `POST /photos/upload/` — Upload a JPEG or PNG image (max 5MB)
- `GET /photos/list/` — List all uploaded photos sorted by date (newest first)
- `GET /photos/{filename}` — Retrieve a specific photo by filename

### ✅ Validation & Security

- Only `image/jpeg` and `image/png` allowed (HTTP **400** on invalid type)
- File size limit: **5MB** enforced during streaming (HTTP **413** on exceed)
- PIL `image.verify()` to reject corrupted or fake images (HTTP **400**)
- Filenames sanitized via regex + UUID suffix to prevent conflicts
- `Path(filename).name` to block path traversal attacks

### 🛠 Libraries

`fastapi`, `uvicorn`, `pillow`
</details>
---
<details>
<summary>🔹 <b>hw_44 — Real-time WebSocket Chat with Moderation</b></summary>

Асинхронний чат у реальному часі на базі WebSockets з інтегрованою системою модерації, цензурою та JWT-автентифікацією.

### 🚀 Features

- **Real-time WebSockets**: Миттєвий обмін повідомленнями без перезавантаження сторінки.
- **Advanced Moderation**: Система команд для адміністраторів та модераторів (`/mute`, `/ban`, `/set_moder`, `/warn`, `/kick`).
- **Censorship Engine**: Автоматична фільтрація нецензурної лексики (EN/RU) з нормалізацією тексту (заміна схожих символів: `0` → `o`, `@` → `a`).
- **JWT Auth**: Повноцінна реєстрація та вхід з використанням Bearer-токенів.
- **Connection Management**: Відстеження активних користувачів, обробка відключень та системні сповіщення (приєднання/вихід).
- **Modern UI**: Адаптивний інтерфейс у стилі "JetBrains Mono" з підтримкою автодоповнення команд через Tab.

### 📡 Endpoints & Commands

**HTTP / Auth**

- `POST /signup` — Реєстрація нового користувача (перший користувач `admin` отримує права адміна).
- `POST /token` — Отримання JWT-токену для підключення.
- `GET /` — Головна сторінка чату (Jinja2).

**WebSocket**

- `WS /ws?token={token}` — Основний шлюз для обміну повідомленнями.

**Chat Commands (🔒 Moder/Admin only)**

- `/mute <username> <min>` — Тимчасове обмеження права писати в чат.
- `/kick <username> <purpose>` — Розірвання активного з'єднання користувача з чатом з причиною.
- `/warn <username>` — Надання зауваження користувачу, після 3 заувжень мут на 10 хвилин.
- `/ban <username>` — Повне блокування користувача з розірванням активного з'єднання.
- `/set_moder <username> True/False` — (Тільки адмін) Призначення або зняття прав модератора.
- `/help` — Список доступних команд.

### ✅ Logic & Validation

- **Normalization**: Цензор ігнорує регістр, спецсимволи та обходить спроби замаскувати слова цифрами.
- **Persistence**: Збереження стану мутів та банів у пам'яті сервера (In-memory).
- **Security**: Хешування паролів через `pwdlib` та перевірка терміну дії токена при кожному WS-підключенні.

### 🛠 Libraries

`fastapi`, `uvicorn`, `PyJWT`, `pwdlib`, `jinja2`, `requests`, `unicodedata`
</details>
---
<details>
<summary>🔹 <b>hw_46_1 — FastAPI User Dashboard</b></summary>

REST API для агрегації даних користувача з зовнішнього джерела (JSONPlaceholder).

### 🚀 Features

- Паралельні HTTP-запити через `ThreadPoolExecutor`
- Агрегація постів, альбомів та фото користувача
- Обробка помилок із логуванням (timeout / HTTP-помилки)
- Вимірювання часу виконання запиту

### 📡 Endpoints

- `GET /user-dashboard/{user_id}` — Повертає профіль користувача, кількість постів, альбомів і фото

### ✅ Validation & Error Handling

- `404` якщо користувача не знайдено в зовнішньому API
- Логування помилок окремо для timeout та HTTP-помилок сервера

### 🛠 Libraries

`fastapi`, `uvicorn`, `requests`

</details>

---

<details>
<summary>🔹 <b>hw_46_2 — FastAPI CPU-Bound Calculator</b></summary>

Async REST API для важких обчислень із використанням `ProcessPoolExecutor` та паралельної обробки.

### 🚀 Features

- Паралельне виконання CPU-bound задач у окремих процесах
- Чанкова обробка великих даних (простих чисел, статистики)
- Валідація вхідних даних через Pydantic v2 (`field_validator`, `model_validator`)
- Таймаут на виконання кожної операції

### 📡 Endpoints

- `POST /calculate` — Виконати обчислення (factorial / primes / matrix / stats)

### ✅ Operations

- `factorial` — Факторіал числа до 1000, повертає результат і кількість цифр
- `primes` — Усі прості числа в діапазоні до 10 000 000 (паралельно по чанках)
- `matrix` — Множення двох випадкових матриць розміром до 200×200 (numpy)
- `stats` — Mean / median / std для масиву до 1 000 000 елементів (numpy)

### ✅ Validation & Error Handling

- `408` при перевищенні таймауту обчислення
- Заборона `NaN` / `Inf` у масиві
- Перевірка обов'язкових полів залежно від операції

### 🛠 Libraries

`fastapi`, `uvicorn`, `pydantic`, `numpy`

</details>
---
<details>
<summary>🔹 <b>hw_54 — TechHub: Django Blog & Portfolio Portal</b></summary>

Веб-портал на Django, який інтегрує технічний блог (TechBlog) та персональне портфоліо розробника (Developer Portfolio).

### 🚀 Features

- **Root Portal Landing**: Єдина точка входу (`/`), яка дозволяє користувачеві перейти до Блогу або Портфоліо.
- **TechBlog (App `blog`)**:
  - Головна сторінка з описом та динамічним вітанням.
  - Сторінка "Про нас" із детальними відомостями про команду та статистикою.
  - Сторінка контактів із посиланнями на соціальні мережі, робочим графіком та адресою.
  - "Популярні статті" з відображенням списку постів та кількості їх переглядів.
  - Інтерактивна форма оцінки досвіду розробника (POST-запит), яка показує результат на основі введених років.
- **Advanced Django Admin Integration (blog)**:
  - Спеціалізований інтерфейс для статей `Article` з редагованим полем `is_featured`, детальними фільтрами, пошуком та полями лише для читання (`views`, `likes`).
  - Кастомні адміністративні дії (Actions):
    - *Позначити як Featured* — швидке встановлення прапорця для обраних статей.
    - *Скинути лічильник переглядів* — обнулення лічильника `views` для виділених постів.
    - *Експорт вибраних статей у CSV* — динамічна генерація та завантаження CSV-файлу з метаданими обраних записів.
  - Кастомізоване керування тегами `Tag` з інтегрованим колірним селектором (color picker) та HTML-безпечним відображенням колірного прев'ю у списку (`color_preview`).
- **Portfolio (App `portfolio`)**:
  - Інформативний кабінет розробника: ім'я, вік, детальна біографія та роль.
  - Структуроване відображення навичок (Frontend та Python) із прогрес-барами та детальними піднавичками.
  - Галерея розроблених проєктів (Flask Restaurant, Django Repair Service, FastAPI Telegram Bot, Copytrading Bot) із технологічним стеком, описом та емодзі.
- **Responsive UI**: Сучасний мінімалістичний дизайн із використанням глобальної CSS-системи та змінних.

### 📡 Endpoints

**Root**
- `GET /` — Головна сторінка-портал (TechHub)

**TechBlog**
- `GET /blog/` — Головна сторінка блогу
- `GET /blog/about/` — Про команду та проєкт
- `GET /blog/contact/` — Контакти та соціальні мережі
- `GET /blog/popular/` — Список популярних статей
- `POST /blog/experience/` / `GET /blog/experience/` — Перевірка досвіду користувача через форму

**Portfolio**
- `GET /portfolio/` — Головна сторінка портфоліо з біографією, навичками та проєктами

### 🛠 Libraries

`django`, `whitenoise`

</details>

---

<details>
<summary>🔹 <b>hw_56 — Library Management System (Django Models & Admin)</b></summary>

Система управління бібліотекою на Django, що демонструє проєктування реляційної бази даних, складні зв'язки в ORM та детальну кастомізацію Django Admin.

### 🚀 Features

- **Relational DB Design**:
  - **Автори (`Author`)**: Зберігання імені, країни та року народження.
  - **Книги (`Book`)**: Зв'язок One-to-Many з автором, унікальний ISBN (`unique=True`), кількість сторінок, рік публікації та статус доступності.
  - **Читачі (`Reader`)**: Зв'язок Many-to-Many з книгами через проміжну модель позики (`Loan`).
  - **Позики (`Loan`)**: Проміжний зв'язок (through-model) з фіксацією дати позики (`loan_date`, автозаповнення) та дати повернення (`return_date`).
- **Customized Django Admin Panel**:
  - **Автори (`AuthorAdmin`)**: Відображення імені, країни та року народження; фільтрація за країною та роком; пошук за ім'ям та країною; сортування за алфавітом.
  - **Книги (`BookAdmin`)**: Відображення основних полів та статусу доступності; фільтрація за автором, роком та доступністю; швидкий пошук за назвою, ISBN чи ім'ям автора; сортування за роком публікації (від новіших).
  - **Читачі (`ReaderAdmin`)**: Перегляд імені та email; пошук за ключовими даними; сортування за алфавітом.
  - **Позики (`LoanAdmin`)**: Повний моніторинг позичених книг з відображенням дат позики та повернення; фільтрація за датами та автором книги; пошук за даними читача (ім'я/email), назвою книги та її автором; сортування за датою позики (від останніх).
- **ORM & Meta constraints**:
  - Використання `verbose_name` та `verbose_name_plural` для локалізованого відображення моделей та полів в адмін-панелі.
  - Налаштування Meta `ordering` для коректного замовчування списків у базі даних.

### 🗄 Models

- `Author`
- `Book` ↔ `Author` (ForeignKey)
- `Reader` ↔ `Book` (ManyToManyField через `Loan`)
- `Loan` (ForeignKey на `Reader` та `Book`)

### 🛠 Libraries

`django`

</details>

---

<details>
<summary>🔹 <b>hw_58 — Course Selection & Student Enrollment System (Django Forms & Validation)</b></summary>

Веб-платформа на Django для вибору навчальних курсів учнями (віком 12-18 років), що демонструє складну валідацію форм (ModelForm), роботу з наборами форм (ModelFormSet) та глибоке налаштування Django Admin для проміжних моделей Many-to-Many.

### 🚀 Features

- **Advanced Form Validation**:
  - **ExtendedUserCreationForm**: Розширена форма реєстрації на базі `UserCreationForm` з обов'язковими полями `email`, `first_name`, `last_name`, `age` та необов'язковим `phone`.
  - **Кастомні валідатори (clean_*)**:
    - `age` — суворе обмеження віку від 12 до 18 років (включно).
    - `phone` — очищення від спецсимволів та валідація унікального українського номера телефону у форматі `+380XXXXXXXXX`.
    - `email` — приведення до нижнього регістру, перевірка унікальності та заборона використання тестових адрес (`@test.com`).
    - `first_name` & `last_name` — перевірка на мінімальну довжину (2 символи), відповідність шаблону букв (з урахуванням апострофів та дефісів) та автоматичне приведення до формату Title Case.
    - `clean` (global) — запобігання збігу логіна (`username`) з ім'ям (`first_name`) користувача.
- **Dynamic Formsets & Inline Course Selection**:
  - **UserCourseFormSet**: Динамічний набір форм для одночасного вибору до 3 курсів із зазначенням пріоритету (Низький, Середній, Високий).
  - **Валідація набору форм (clean)**:
    - Заборона вибору одного й того самого курсу більше ніж один раз.
    - Обов'язкова унікальність пріоритетів серед обраних курсів (пріоритети не повинні збігатися).
- **Customized Django Admin Panel**:
  - **Курси (`CourseAdmin`)**: Відображення списку курсів (назва, тривалість, оцінка) з фільтрацією за тривалістю та пошуком за назвою та оцінкою. Включає вбудований табличний інтерфейс (`UserCourseInline`) для перегляду та редагування обраних користувачами курсів прямо на сторінці курсу.
  - **Обрані курси (`UserCourseAdmin`)**: Табличне відображення зв'язків користувач-курс із вказанням пріоритету та дати вибору. Підтримує пошук за ім'ям/email користувача та назвою курсу, а також `raw_id_fields` для зручного вибору зв'язків у великих базах даних.
- **Responsive Premium UI**:
  - Головна сторінка зі списком курсів, динамічною навігацією та кнопками авторизації.
  - Інформативна та візуально досконала сторінка особистого кабінету учня (профіль) з генерацією аватара по першій літері імені та повними відомостями про акаунт.
  - Панель навчання (дешборд) з переліком обраних курсів, детальною інформацією (тривалість, оцінка, дата подачі заявки) та яскравими бейджами пріоритетів, відсортованими за пріоритетом.

### 📡 Endpoints

- `GET /` — Головна сторінка платформи зі списком навчальних програм (Course Grid)
- `GET /register/` / `POST /register/` — Сторінка реєстрації з одночасною валідацією даних учня та набору форм вибору курсів
- `GET /login/` — Стандартна сторінка автентифікації
- `GET /profile/` — Особистий кабінет з персональними даними учня (🔒)
- `GET /dashboard/` — Панель навчання зі списком обраних програм та пріоритетів (🔒)

### 🗄 Models

- `User` (AbstractUser) — розширена модель користувача з унікальними полями `age` та `phone`
- `Course` — модель навчального курсу (назва, тривалість, оцінка)
- `UserCourse` (through-model) — проміжна таблиця для Many-to-Many з додатковими даними (пріоритет вибору, дата створення)

### 🛠 Libraries

`django`

</details>

---
## 🎯 Goal
The goal of this repository is to improve backend development skills through building real-world applications using:
- ⚙️ Flask ecosystem  
- ⚡ FastAPI  
- 🦄 Django framework  
- 🗄 SQLAlchemy & Django ORM  
- 🧪 Testing practices  
---
## ⭐ Future Improvements
- Add Docker support
- Deploy projects (Render / VPS)
- Add API documentation (Swagger / Redoc)
- Improve frontend UI
