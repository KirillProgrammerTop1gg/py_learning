from django.urls import path
from . import views

app_name = 'project_gallery'

urlpatterns = [
    path('', views.project_list, name='index'),
    path('add/', views.add_project, name='add_project'),
    path('add-images/', views.add_images, name='add_images'),
]
