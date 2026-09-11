# Django Blog Optimization Project

A simple, secure, and optimized blog application built with Django. This project was created to demonstrate core Django features, security best practices, and database/caching optimizations.

## Technologies Used
* **Python 3**
* **Django**
* **SQLite** (Default)
* **Django Debug Toolbar** (for query profiling)

## Project Requirements & Implementation

### 1. Basic Application Structure
* **Django Project Structure**: A main project `blog_project` with a modular `blog` application.
* **Models**: 
  * `Post`: Stores the author (ForeignKey to User), title, content (text), and publication date.
  * `Comment`: Associated with a specific post, storing the author and text content.
* **Pages & Views**: 
  * **Post List Page**: Displays all published posts.
  * **Post Detail Page**: Shows a specific post along with its associated comments.
  * **Comment Form**: Allows authenticated users to add comments on the post detail page.
* **Authentication**: Utilizes built-in Django views for user registration, login, and logout.
* **Initial Data**: The database is pre-populated with test posts (from various authors) and 3-4 comments for each post.

### 2. Security Enhancements
* **Secure Settings Configuration**: 
  * `DEBUG = False` (for production readiness).
  * `SECRET_KEY` is safely loaded from environment variables (`.env`).
  * Cookies are secured via `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`.
* **Robust Form Validation & Sanitization**: 
  * Comments are strictly limited to a maximum of 500 characters.
  * HTML tags are forbidden and stripped to prevent Cross-Site Scripting (XSS). *Testing `<script>alert('test')</script>` will successfully block or sanitize the input.*
* **Rate Limiting**: 
  * Implemented a restriction of a maximum of 3 comments per 5 minutes per user to prevent spam and abuse.

### 3. Optimization and Performance
* **Query Profiling**: 
  * Integrated **Django Debug Toolbar** to track, analyze, and minimize the number of SQL queries per page.
* **Database Optimization (Fixing N+1 Problems)**:
  * Used `select_related('author')` on the posts list page to fetch post authors in a single SQL query, avoiding the N+1 query problem.
  * Applied `prefetch_related('comments__author')` on the post detail page to efficiently load comments and their respective authors in bulk.
* **Caching Mechanisms**:
  * **View Caching**: The post list view is cached for 5 minutes using the `@cache_page(300)` decorator.
  * **Template Fragment Caching**: The sidebar is cached for 10 minutes directly in the Django template using `{% cache 600 sidebar %}`.
* **Cache Invalidation**: 
  * Configured Django Signals (`post_save` on the `Post` model) to automatically clear the relevant cache whenever a new `Post` is created, ensuring users always see up-to-date content without waiting for the cache to expire naturally.

## Setup Instructions

1. **Clone or Download the Repository**
2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install django django-debug-toolbar python-dotenv
   ```
4. **Environment Variables**:
   Create a `.env` file in the root directory alongside `manage.py` and add your secret key:
   ```env
   SECRET_KEY=your_secure_secret_key_here
   ```
5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
6. **Create a Superuser (Optional)**:
   ```bash
   python manage.py createsuperuser
   ```
7. **Start the Development Server**:
   ```bash
   python manage.py runserver --insecure
   ```
   *(Note: `--insecure` is needed to serve static files when `DEBUG = False` locally)*

## How to Test Features
* **XSS Prevention**: Try adding `<script>alert('test')</script>` as a comment text. It will either be rejected by validation or sanitized.
* **Rate Limiting**: Try posting 4 comments within a 5-minute window. The 4th comment should return a validation error or block message.
* **N+1 Optimization & Toolbar**: Open the application in the browser and use the Django Debug Toolbar on the right side of the screen to inspect the number of executed SQL queries on the list and detail pages. You should see a highly optimized query count.
* **Cache Invalidation**: Open the post list page. Then create a new post via the Django Admin panel. Refresh the post list page to verify that the cache was successfully cleared and the new post appears immediately.
