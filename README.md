# 🐍 Python Learning Repository

This repository contains my Python backend learning projects built with **Flask** and **FastAPI**.

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

## 🎯 Goal

The goal of this repository is to improve backend development skills through building real-world applications using:

- ⚙️ Flask ecosystem  
- ⚡ FastAPI  
- 🗄 SQLAlchemy  
- 🧪 Testing practices  

---

## ⭐ Future Improvements

- Add Docker support
- Deploy projects (Render / VPS)
- Add API documentation (Swagger / Redoc)
- Improve frontend UI
