from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('', views.home, name = 'base'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('skills/', views.SkillsListView.as_view(), name='skills_list'),
    path('skills/<int:pk>/', views.SkillsDetailView.as_view(), name='skills_detail'),
    path('experience/', views.ExperienceListView.as_view(), name='experience_list'),
    path('experience/<int:pk>/', views.ExperienceDetailView.as_view(), name='experience_detail'),
]