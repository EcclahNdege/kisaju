from django.urls import path

from . import views

urlpatterns = [
    path('logs/', views.log_list, name='log_list'),
    path('logs/new/', views.log_create, name='log_create'),
]
