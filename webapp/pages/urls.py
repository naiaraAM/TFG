# pages/urls.py

from django.urls import path
from pages import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('APT_samples/', views.samples_index, name='samples_index'),
    path('APT_samples/<str:pk>/', views.sample_detail, name='sample_detail'),
]