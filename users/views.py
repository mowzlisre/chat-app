from django.shortcuts import render, redirect
from django.contrib.auth.views import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

def LoginView(request):
    error_message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                error_message = "Your account has not been verified"
        else:
            error_message = "Incorrect username or password."
    return render(request, 'login.html', {"errors": error_message})

def LogoutView(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out. Please login to continue!')
    return redirect('login')