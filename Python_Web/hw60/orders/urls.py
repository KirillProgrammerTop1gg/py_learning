from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.user_orders_view, name='list'),
    path('create/', views.create_order_view, name='create'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
