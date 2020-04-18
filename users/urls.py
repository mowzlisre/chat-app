from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView, name="login"),
    path('logout/', LogoutView, name="logout")
]
