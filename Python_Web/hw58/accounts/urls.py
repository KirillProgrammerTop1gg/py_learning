from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_view, register_view, profile_view, dashboard

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
]


