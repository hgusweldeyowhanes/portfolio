from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('projects/', views.project_list, name="project_list"),
    path('projects/<slug:slug>/', views.project_detail, name="project_detail"),
    path('skills/', views.skills_list, name="skills_list"),
    path('experience/', views.experience_list, name="experience_list"),
]
