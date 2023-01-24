from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.main_page),
    path('your_metro/', views.your_metro),
]
