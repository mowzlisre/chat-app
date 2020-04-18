from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth.views import login_required

@login_required
def home(request):
    return render(request, 'app/home.html')

@login_required
def classes(request):
    context = {
        "classes": Class.objects.filter(members=request.user),
    }
    return render(request, 'app/classes.html', context)

@login_required()
def messages(request, pk):
    x = Class.objects.get(id=pk)
    context = {
        "class": Class.objects.get(id=pk),
    }
    if request.method == "POST":
        message = Messages()
        message.user = User.objects.get(id=request.user.id)
        message.id = get_random_string(128).lower()
        msg = request.POST.get('message')
        if msg.replace(' ','').strip() != '':
            obj = Class.objects.get(id=pk)
            message.messages = msg
            message.save()
            obj.texts.add(message)
            obj.save()
        

    return render(request, 'app/messages.html', context)
    