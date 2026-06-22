from django.urls import path
from . import views


# Простір імен для додатку, щоб уникнути конфліктів з іншими додатками
app_name = 'portfolio'


urlpatterns = [
    # Головна сторінка блогу
    path('', views.home_view, name='home'),

]

