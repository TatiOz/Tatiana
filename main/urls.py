from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('skills/', views.skills, name='skills'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('impressum/', views.impressum, name='impressum'),
    path('cookies/', views.cookies, name='cookies'),
    path('sitemap/', views.sitemap_page, name='sitemap'),
]