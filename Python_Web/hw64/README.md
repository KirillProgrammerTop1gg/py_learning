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
<summary>🔹 <b>hw_22 — Sfera: Social Messenger</b></summary>

Flask-based social network with a messaging system.

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

Async REST API for a skill-exchange platform with JWT authentication and extended statistics.

### 🚀 Features

- Full CRUD for users, skills, categories, exchanges, and reviews
- JWT authentication via Bearer token (`PyJWT`)
- Route-level permission checks (owner / admin)
- Skill-exchange system with statuses: `pending → accepted → completed`
- Reviews allowed only after a completed exchange, no duplicates
- Skill search by name/description, filtering by category
- Statistics: top skills, most active users, exchange success rate
- Async SQLAlchemy + asyncpg, `selectinload` for eager-loading relationships

### 📡 Endpoints

**auth**

- `POST /token` — Get a JWT token by username

**users**

- `POST /api/users/` — Register a user
- `GET /api/users/` — List users
- `GET /api/users/me` — Own profile (🔒)
- `GET /api/users/{user_id}` — User profile
- `PUT /api/users/me` — Update own profile (🔒)
- `PUT /api/users/{user_id}` — Update profile (🔒 owner or admin)
- `GET /api/users/{user_id}/skills` — User's skills

**categories**

- `GET /api/categories/` — List categories (with skill counts)
- `GET /api/categories/{id}` — Category by ID
- `GET /api/categories/slug/{slug}` — Category by slug
- `GET /api/categories/{id}/skills` — Category with all its skills
- `POST /api/categories/` — Create a category (🔒)
- `PUT /api/categories/{id}` — Update a category (🔒)
- `DELETE /api/categories/{id}` — Delete a category (🔒, not possible if it has skills)

**skills**

- `GET /api/skills/` — List skills (filters: `category_id`, `can_teach`, `want_learn`, `search`)
- `GET /api/skills/{id}` — Skill by ID
- `POST /api/skills/` — Create a skill (🔒)
- `PUT /api/skills/{id}` — Update a skill (🔒)
- `DELETE /api/skills/{id}` — Delete a skill (🔒)
- `GET /api/skills/{id}/matches` — Find matches for an exchange

**exchanges**

- `GET /api/exchanges/` — List exchanges (filters: `status`, `user_id`, `from_date`, `to_date`, `sort_order`)
- `GET /api/exchanges/my/sent` — Sent requests (🔒)
- `GET /api/exchanges/my/received` — Received requests (🔒)
- `GET /api/exchanges/{id}` — Exchange details (🔒)
- `POST /api/exchanges/` — Create an exchange request (🔒)
- `PUT /api/exchanges/{id}` — Update exchange status (🔒)

**reviews**

- `GET /api/reviews/` — List reviews
- `GET /api/reviews/{id}` — Review by ID
- `GET /api/reviews/user/{user_id}` — Reviews about a user
- `GET /api/reviews/user/{user_id}/rating` — User's average rating
- `POST /api/reviews/` — Leave a review (🔒, only after a completed exchange)

**stats**

- `GET /api/stats/top-skills` — Top skills by number of users
- `GET /api/stats/active-users` — Most active users
- `GET /api/stats/exchange-success-rate` — Exchange success-rate statistics

### ✅ Validation & Business Logic

- `can_teach` and `want_learn` cannot both be `true` for the same skill
- Exchanging with oneself is forbidden (HTTP **400**)
- Only the receiver can accept/decline an exchange; either participant can cancel it
- A review can only be left if the exchange status is `completed` (HTTP **400** otherwise)
- A repeated review on the same exchange from the same user is forbidden
- Deleting a category with linked skills → HTTP **409 Conflict**
- Category slug is validated with a regular expression: `^[a-z0-9]+(?:-[a-z0-9]+)*$`

### 🔐 Authentication

JWT token in the `Authorization: Bearer <token>` header. The token contains `user_id` and `role`.
For testing: `POST /token` with `{"user_id": 1, "role": "user"}`.

### 🗄 Models

`User` ↔ `Skill` (many-to-many via `skill_user_association`)
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

Real-time async chat built on WebSockets with an integrated moderation system, profanity filtering, and JWT authentication.

### 🚀 Features

- **Real-time WebSockets**: Instant message exchange without page reloads.
- **Advanced Moderation**: Command system for admins and moderators (`/mute`, `/ban`, `/set_moder`, `/warn`, `/kick`).
- **Censorship Engine**: Automatic profanity filtering (EN/RU) with text normalization (replacing look-alike characters: `0` → `o`, `@` → `a`).
- **JWT Auth**: Full registration and login using Bearer tokens.
- **Connection Management**: Tracking of active users, disconnect handling, and system notifications (join/leave).
- **Modern UI**: Responsive interface in a "JetBrains Mono" style with Tab-based command autocompletion.

### 📡 Endpoints & Commands

**HTTP / Auth**

- `POST /signup` — Register a new user (the first user, `admin`, gets admin rights)
- `POST /token` — Obtain a JWT token for connecting
- `GET /` — Chat home page (Jinja2)

**WebSocket**

- `WS /ws?token={token}` — Main gateway for message exchange

**Chat Commands (🔒 Moder/Admin only)**

- `/mute <username> <min>` — Temporarily restrict a user's ability to post in chat
- `/kick <username> <purpose>` — Disconnect a user's active chat connection, with a reason
- `/warn <username>` — Issue a warning to a user; after 3 warnings, a 10-minute mute is applied
- `/ban <username>` — Fully ban a user and terminate their active connection
- `/set_moder <username> True/False` — (Admin only) Grant or revoke moderator rights
- `/help` — List available commands

### ✅ Logic & Validation

- **Normalization**: The filter ignores case and special characters, and defeats attempts to mask words with digits.
- **Persistence**: Mute and ban state is kept in server memory (in-memory).
- **Security**: Passwords are hashed with `pwdlib`, and token expiration is checked on every WS connection.

### 🛠 Libraries

`fastapi`, `uvicorn`, `PyJWT`, `pwdlib`, `jinja2`, `requests`, `unicodedata`

</details>

---

<details>
<summary>🔹 <b>hw_46_1 — FastAPI User Dashboard</b></summary>

REST API that aggregates user data from an external source (JSONPlaceholder).

### 🚀 Features

- Parallel HTTP requests via `ThreadPoolExecutor`
- Aggregation of a user's posts, albums, and photos
- Error handling with logging (timeouts / HTTP errors)
- Request execution time measurement

### 📡 Endpoints

- `GET /user-dashboard/{user_id}` — Returns the user's profile and the number of posts, albums, and photos

### ✅ Validation & Error Handling

- **404** if the user is not found in the external API
- Errors are logged separately for timeouts and server HTTP errors

### 🛠 Libraries

`fastapi`, `uvicorn`, `requests`

</details>

---

<details>
<summary>🔹 <b>hw_46_2 — FastAPI CPU-Bound Calculator</b></summary>

Async REST API for heavy computations using `ProcessPoolExecutor` and parallel processing.

### 🚀 Features

- Parallel execution of CPU-bound tasks in separate processes
- Chunked processing of large data (primes, statistics)
- Input validation via Pydantic v2 (`field_validator`, `model_validator`)
- Timeout for each operation

### 📡 Endpoints

- `POST /calculate` — Run a computation (factorial / primes / matrix / stats)

### ✅ Operations

- `factorial` — Factorial of a number up to 1000; returns the result and its digit count
- `primes` — All primes in a range up to 10,000,000 (processed in parallel chunks)
- `matrix` — Multiplication of two random matrices up to 200×200 (numpy)
- `stats` — Mean / median / std for an array of up to 1,000,000 elements (numpy)

### ✅ Validation & Error Handling

- **408** when the computation timeout is exceeded
- `NaN` / `Inf` values in the array are rejected
- Required fields are checked based on the operation

### 🛠 Libraries

`fastapi`, `uvicorn`, `pydantic`, `numpy`

</details>

---

<details>
<summary>🔹 <b>hw_54 — TechHub: Django Blog & Portfolio Portal</b></summary>

A Django web portal that integrates a technical blog (TechBlog) and a developer's personal portfolio (Developer Portfolio).

### 🚀 Features

- **Root Portal Landing**: A single entry point (`/`) that lets users navigate to the Blog or the Portfolio.
- **TechBlog (App `blog`)**:
  - Home page with a description and a dynamic greeting.
  - An "About us" page with detailed team information and statistics.
  - A contact page with social media links, working hours, and address.
  - A "Popular articles" page listing posts and their view counts.
  - An interactive developer-experience assessment form (POST request) that shows a result based on the entered years.
- **Advanced Django Admin Integration (blog)**:
  - A specialized interface for `Article` with an editable `is_featured` field, detailed filters, search, and read-only fields (`views`, `likes`).
  - Custom admin actions:
    - *Mark as Featured* — quickly flags selected articles.
    - *Reset view count* — zeroes the `views` counter for selected posts.
    - *Export selected articles to CSV* — dynamically generates and downloads a CSV file with the metadata of selected records.
  - Custom `Tag` management with an integrated color picker and an HTML-safe color preview in the list view (`color_preview`).
- **Portfolio (App `portfolio`)**:
  - An informative developer profile: name, age, detailed bio, and role.
  - Structured skill display (Frontend and Python) with progress bars and detailed sub-skills.
  - A gallery of built projects (Flask Restaurant, Django Repair Service, FastAPI Telegram Bot, Copytrading Bot) with their tech stack, description, and emoji.
- **Responsive UI**: Modern, minimalist design using a global CSS system and variables.

### 📡 Endpoints

**Root**

- `GET /` — Portal home page (TechHub)

**TechBlog**

- `GET /blog/` — Blog home page
- `GET /blog/about/` — About the team and the project
- `GET /blog/contact/` — Contacts and social media
- `GET /blog/popular/` — List of popular articles
- `POST /blog/experience/` / `GET /blog/experience/` — Check user experience via a form

**Portfolio**

- `GET /portfolio/` — Portfolio home page with bio, skills, and projects

### 🛠 Libraries

`django`, `whitenoise`

</details>

---

<details>
<summary>🔹 <b>hw_56 — Library Management System (Django Models & Admin)</b></summary>

A Django library management system demonstrating relational database design, complex ORM relationships, and detailed Django Admin customization.

### 🚀 Features

- **Relational DB Design**:
  - `Author`: stores name, country, and year of birth.
  - `Book`: One-to-Many relationship with `Author`, unique ISBN (`unique=True`), page count, publication year, and availability status.
  - `Reader`: Many-to-Many relationship with books via the intermediate loan model (`Loan`).
  - `Loan`: an intermediate (through-model) relationship recording the loan date (`loan_date`, auto-filled) and the return date (`return_date`).
- **Customized Django Admin Panel**:
  - `AuthorAdmin`: displays name, country, and year of birth; filtering by country and year; search by name and country; alphabetical ordering.
  - `BookAdmin`: displays the main fields and availability status; filtering by author, year, and availability; quick search by title, ISBN, or author name; ordered by publication year (newest first).
  - `ReaderAdmin`: view of name and email; search by key fields; alphabetical ordering.
  - `LoanAdmin`: full tracking of borrowed books with loan and return dates; filtering by date and book author; search by reader data (name/email), book title, and author; ordered by loan date (most recent first).
- **ORM & Meta constraints**:
  - Use of `verbose_name` and `verbose_name_plural` for localized display of models and fields in the admin panel.
  - `Meta.ordering` configured for correct default list ordering.

### 🗄 Models

- `Author`
- `Book` ↔ `Author` (ForeignKey)
- `Reader` ↔ `Book` (ManyToManyField via `Loan`)
- `Loan` (ForeignKey to `Reader` and `Book`)

### 🛠 Libraries

`django`

</details>

---

<details>
<summary>🔹 <b>hw_58 — Course Selection & Student Enrollment System (Django Forms & Validation)</b></summary>

A Django web platform for students (aged 12–18) to select courses, demonstrating complex form validation (`ModelForm`), formset handling (`ModelFormSet`), and in-depth Django Admin customization for Many-to-Many through-models.

### 🚀 Features

- **Advanced Form Validation**:
  - `ExtendedUserCreationForm`: an extended registration form based on `UserCreationForm`, with required `email`, `first_name`, `last_name`, `age` fields and an optional `phone` field.
  - **Custom validators (`clean_*`)**:
    - `age` — strictly limited to 12–18 years old (inclusive).
    - `phone` — strips special characters and validates a unique Ukrainian phone number in the `+380XXXXXXXXX` format.
    - `email` — normalized to lowercase, checked for uniqueness, and test addresses (`@test.com`) are rejected.
    - `first_name` & `last_name` — checked for minimum length (2 characters), matched against a letters-only pattern (allowing apostrophes and hyphens), and auto-converted to Title Case.
    - `clean` (global) — prevents the username from matching the user's `first_name`.
- **Dynamic Formsets & Inline Course Selection**:
  - `UserCourseFormSet`: a dynamic formset for selecting up to 3 courses at once, each with a priority (Low, Medium, High).
  - **Formset validation (`clean`)**:
    - Selecting the same course more than once is forbidden.
    - Priorities among selected courses must be unique (no duplicates allowed).
- **Customized Django Admin Panel**:
  - `CourseAdmin`: lists courses (title, duration, rating) with filtering by duration and search by title and rating. Includes an inline tabular interface (`UserCourseInline`) for viewing and editing users' selected courses directly on the course page.
  - `UserCourseAdmin`: a tabular view of user-course links showing priority and selection date. Supports search by user name/email and course title, plus `raw_id_fields` for convenient relation selection in large databases.
- **Responsive Premium UI**:
  - A home page listing courses, with dynamic navigation and auth buttons.
  - An informative, polished student profile page with an avatar generated from the first letter of the name and full account details.
  - A learning dashboard listing selected courses with detailed info (duration, rating, application date) and bright priority badges, sorted by priority.

### 📡 Endpoints

- `GET /` — Platform home page listing courses (Course Grid)
- `GET /register/` / `POST /register/` — Registration page validating both the student's data and the course-selection formset simultaneously
- `GET /login/` — Standard authentication page
- `GET /profile/` — Student profile with personal data (🔒)
- `GET /dashboard/` — Learning dashboard listing selected courses and priorities (🔒)

### 🗄 Models

- `User` (AbstractUser) — extended user model with unique `age` and `phone` fields
- `Course` — course model (title, duration, rating)
- `UserCourse` (through-model) — an intermediate table for the Many-to-Many relation with extra data (selection priority, creation date)

### 🛠 Libraries

`django`

</details>

---

<details>
<summary>🔹 <b>hw_60 — DevPortfolio: Client Orders Portal, Blog & Live Analytics (Django Multi-app & Email Notification System)</b></summary>

A Django web portal combining a developer's personal portfolio (Developer Portfolio), a technical blog (TechBlog), and an interactive client order/brief system (Client Orders Platform), with automatic email notifications and a custom business-analytics dashboard.

### 🚀 Features

- **Interactive Client Orders Platform (App `orders`)**:
  - Submission of detailed project briefs (project type, budget in USD, desired timeline, spec description, contact info).
  - User registration and authentication with form-level validation for unique username and email.
  - A client dashboard listing their briefs, current statuses ("Pending review", "In development", "Completed", "Cancelled"), and the ability to leave a review after a successfully completed order.
- **Automated HTML Email Notification System**:
  - **For the admin**: an automatic detailed HTML email (with a plain-text fallback) is sent to superusers when a new brief is created, containing all submitted client data and a direct link to the order in Django Admin.
  - **For the client**: an instant, styled HTML email is sent whenever the admin changes their brief's status via Django Admin.
- **Advanced Admin Dashboard & Live Analytics**:
  - A dedicated dashboard at `/orders/profile/` that renders a custom interface depending on the user's role:
    - **For clients**: simple statistics on their orders.
    - **For staff/superusers**: a full business-analytics dashboard showing the top 10 most-visited pages, the top 5 popular projects, and an ASCII chart of monthly order activity (grouped in Python for database compatibility).
- **Custom Page-View Tracking Middleware (App `portfolio`)**:
  - Custom middleware (`PageViewMiddleware`) that atomically tracks and records the view count for every unique site URL (excluding admin, static, media, and favicon), storing the stats in the `PageView` model.
- **Technical Blog with Search & Comments (App `blog`)**:
  - Article search by keyword (title, category, technology).
  - Automatic transliterated slug generation (Cyrillic-to-Latin) when saving articles.
  - A comment system for logged-in users and an atomic view counter for each blog post.
- **Unified Portfolio Landing with Context Processors**:
  - Global developer configuration (name, role, bio, social links) is loaded from `portfolio_config.json` into every template via a Django context processor.
  - Display of developer skills with dynamic ASCII progress bars, work experience, and a slider of real client testimonials.

### 📡 Endpoints

**Root & Portfolio**

- `GET /` — Portfolio home page (bio, experience, skills, and testimonial slider)
- `GET /projects/` — Gallery and filtering of built projects by technology
- `GET /projects/<id>/` — A project's detail page with a view counter

**TechBlog**

- `GET /blog/` — List of articles with keyword search (`?q=...`)
- `GET /blog/<slug>/` — Article page with a unique-view counter and comment form (🔒 to post)

**Orders & Auth Portal**

- `GET /orders/` — List of the current client's orders/briefs (🔒)
- `GET /orders/create/` / `POST /orders/create/` — New project brief submission form (🔒)
- `GET /orders/profile/` — Client dashboard (🔒) with order history/reviews, or an analytics admin panel for staff
- `GET /orders/register/` / `POST /orders/register/` — New client registration with automatic login
- `GET /orders/login/` / `POST /orders/login/` — User login
- `GET /orders/logout/` — Log out

### 🗄 Models

- **portfolio**:
  - `Category` — categories for skills, technologies, and articles
  - `Technology` — tech stack (linked to a category and multiple projects)
  - `Project` — portfolio projects (title, description, date, link, view count)
  - `Skill` — skills with a proficiency percentage and ASCII visualization
  - `Experience` — work experience (position, company, period, description)
  - `PageView` — atomic page-view logging model
- **blog**:
  - `BlogPost` — posts with a transliterated slug, view counter, and links to categories/technologies
  - `Comment` — user comments on articles
- **orders**:
  - `Order` — user requests/briefs (title, project type, budget, deadlines, description, status, link to `User`)
  - `Review` — a single review for a completed order (One-to-One with `Order`)

### 🛠 Libraries

`django`, `pillow`, `whitenoise`

</details>

---

<details>
<summary>🔹 <b>hw_62 — StudySystem REST API (Django Rest Framework & Query Optimizations)</b></summary>

A REST API for an education platform built on Django REST Framework, with a full permission system, filtering, validation, JWT authorization, automatic Swagger documentation, and database query optimization (solving the N+1 problem).

### 🚀 Features

- **Models & Relations**:
  - `Student` — a student entity (first name, last name, age, email, creation date).
  - `Course` — a course (title, description, duration in hours) with a Many-to-Many relation to `Student`.
  - `Enrollment` — an intermediate table (through-model) linking course and student, recording the exact enrollment date and enforcing uniqueness of the (student, course) pair.
- **Comprehensive Validation**:
  - **Student validation**: first and last names cannot be identical; the combined length of first and last name must be at least 5 characters; students under 18 cannot use corporate email addresses (`@company.com`). Validation supports partial updates (`PATCH`) and a null age value.
  - **Course validation**: prevents the course title from being repeated too many times in its description (more than twice).
- **ViewSets & URL Routing**:
  - Full CRUD operations implemented for all models via `ModelViewSet`.
  - Automatic URL and endpoint generation via `DefaultRouter`.
  - URL-path versioning configured (e.g., `/api/v1/...`).
- **Search & Filtering**:
  - **Search**: flexible student search by first name, last name, or email (`?search=...`).
  - **Filtering**: dynamic course filtering by enrolled student count (`?min_students=...` and `?max_students=...` parameters), based on Django ORM `Count` annotations.
- **Security & Permissions**:
  - A custom `IsStaffOrReadOnly` permission class is integrated.
  - Students and guests have read-only access to courses (`GET`, `OPTIONS`, `HEAD`), while modifying courses (`POST`, `PUT`, `PATCH`, `DELETE`) is restricted to staff users only.
  - JWT authentication is integrated via `SimpleJWT`.
- **Query Optimizations (O(1) Queries)**:
  - `select_related('student')` is used in `Enrollment` queries to minimize related-student lookups.
  - `prefetch_related('enrollments__student', 'students')` is used in `Course` to load related students in a single query, fully eliminating the N+1 problem when serializing course lists. The number of SQL queries stays constant ($O(1)$) regardless of the number of courses.
- **Throttling, Versioning & Swagger Docs**:
  - Rate limits configured: Anon (100/day), User (1000/day), and Scoped "students" (10,000/day).
  - OpenAPI docs generated via `drf-spectacular` — the schema is available at `/api/v1/schema/`, with an interactive Swagger UI at `/api/v1/docs/`.
- **Automated Test Suite**:
  - 9 comprehensive integration tests (`APITestCase`) automatically verify authentication, permissions, filtering and search, custom serializer validation, and SQL query limits.

### 📡 Endpoints

- `GET /api/v1/students/` — List students with `?search=...` (🔒)
- `POST /api/v1/students/` — Create a new student (🔒)
- `GET /api/v1/courses/` — List courses with `?min_students=...` and `?max_students=...` filters
- `POST /api/v1/courses/` — Create a course (🔒 staff only)
- `GET /api/v1/enrollments/` — List enrollments (🔒)
- `POST /api/v1/enrollments/` — Enroll a student in a course (🔒)
- `POST /api/token/` — Obtain JWT tokens (access/refresh)
- `POST /api/token/refresh/` — Refresh the JWT access token
- `GET /api/v1/schema/` — OpenAPI schema (YAML/JSON)
- `GET /api/v1/docs/` — Interactive Swagger UI documentation

### 🗄 Models

- `Student` — student entity (`first_name`, `last_name`, `email`, `age`, `created_at`)
- `Course` — course model (`title`, `description`, `duration`, `students` ManyToMany)
- `Enrollment` — through-model (`student`, `course`, `enrollment_date`)

### 🛠 Libraries

`django`, `djangorestframework`, `django-filter`, `djangorestframework-simplejwt`, `drf-spectacular`

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
