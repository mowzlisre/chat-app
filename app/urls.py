from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('class/', views.classes, name="classes"),
    path('class/<pk>/', views.messages, name="messages"),
]
