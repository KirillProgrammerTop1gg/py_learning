from django.urls import path
from . import views


# Простір імен для додатку, щоб уникнути конфліктів з іншими додатками
app_name = 'blog'


urlpatterns = [
    path('', views.home_view, name='home'),
    path('experience/', views.check_experience, name='experience'),
    path('popular/', views.popular_posts, name='popular'),
    path('about/', views.about_us, name="about"),
    path('contact/', views.contacts, name="contact"),
]

