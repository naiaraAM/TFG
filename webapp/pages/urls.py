# pages/urls.py

from django.urls import path
from pages import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.upload_file, name='upload_file'),
    path('APT_samples/all', views.samples_index, name='samples_index'),
    path('samples/original', views.show_original_samples, name='show_original_samples'),
    path('samples/user_uploaded', views.show_user_uploaded_samples, name='show_user_uploaded_samples'),
    path('APT_samples/<str:pk>', views.sample_detail, name='sample_detail'),
    path('comparison/<str:pk>', views.comparison, name='comparison'),
]