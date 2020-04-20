from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.views import login_required
from django.contrib import messages as msgs


@login_required
def home(request):
    return render(request, 'app/home.html')


@login_required
def classes(request):
    context = {
        "classes": Class.objects.filter(members=request.user),
        "invites": Invite.objects.filter(invitee=request.user)
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
        msg = request.POST.get('message')
        if msg.replace(' ', '').strip() != '':
            obj = Class.objects.get(id=pk)
            message.messages = msg
            message.save()
            obj.texts.add(message)
            obj.save()
    return render(request, 'app/messages.html', context)


@login_required
def new_classroom(request):
    usr = User.objects.get(id=request.user.id)
    if request.method == "POST":
        clss = Class()
        clss.name = request.POST.get('name')
        clss.description = request.POST.get('description')
        clss.creator = usr
        clss.save()
        clss.admin.add(usr)
        clss.members.add(usr)
        clss.save()
        msgs.success(request, 'Your new class ' + clss.name +
                     ' has been created successfully!')
        return redirect('classes')
    return render(request, 'app/new_classroom.html')


@login_required
def classroom_dashboard(request, pk):
    context = {
        "class": Class.objects.get(id=pk),
    }
    return render(request, 'app/classroom_dashboard.html', context)


@login_required
def classroom_settings(request, pk):
    context = {
        "obj": Class.objects.get(id=pk),
    }
    if request.method == "POST":
        clss = Class.objects.get(id=pk)
        clss.name = request.POST.get("name")
        clss.description = request.POST.get("description")
        clss.privacy = request.POST.get("privacy")
        clss.texting = request.POST.get("texting")
        clss.save()
        msgs.success(request, 'Class settings have been updated!')
    return render(request, 'app/class_settings.html', context)

@login_required
def invite_member(request, pk):
    if request.method == "POST":
        clss = Class.objects.get(id=pk)
        invite = Invite()
        invite.inviter = User.objects.get(id=request.user.id)
        usr = User.objects.get(profile__id=request.POST.get("code"))
        if usr in clss.members.all():
            msgs.warning(request, 'It seems the user you are trying to add is already in the class')
            return redirect('classroom-settings', pk=pk)
        else:
            invite.invitee = User.objects.get(profile__id=request.POST.get("code"))
            invite.clss = Class.objects.get(id=pk)
            invite.invalid = False
            invite.save()
            msgs.success(request, str(usr) + ' has been invited to the class!')
            return redirect('classroom-settings', pk=pk)

    return redirect('classroom')

@login_required
def add_member(request, pk, to):
    invite = Invite.objects.get(code=pk)
    context = {
        "invites": invite
    }
    usr = User.objects.get(profile__id=to)
    if request.method == "POST":
        clss = Class.objects.get(id=invite.clss.id)
        clss.members.add(usr)
        clss.save()
        msgs.info(request, 'You have successfully joined the class ' + str(invite.clss))
        invite.invalid = True
        invite.save()
        return redirect('classroom', pk=invite.clss.id)
    return render(request, 'app/invite_page.html', context)

@login_required
def remove_member(request, pk, code):
    usr = User.objects.get(profile__id=code)
    clss = Class.objects.get(id=pk)
    if clss.members.count() == 1:
        msgs.warning(request, 'It seems you are the last person left. You can delete this class instead!')
        return redirect('classroom-settings', pk=pk)
    else:
        clss.members.remove(usr)
        clss.admin.remove(usr)
        clss.save()
        msgs.error(request, str(usr) + ' has been removed from the class!')
        return redirect('classroom-settings', pk=pk)
@login_required
def leave_class(request, pk, code):
    usr = User.objects.get(profile__id=code)
    clss = Class.objects.get(id=pk)
    clss.members.remove(usr)
    clss.admin.remove(usr)
    clss.save()
    msgs.warning(request, 'You have left the class ' + str(clss))
    return redirect('classes')

@login_required
def add_admin(request, pk, code):
    usr = User.objects.get(profile__id=code)
    clss = Class.objects.get(id=pk)
    clss.admin.add(usr)
    clss.save()
    msgs.success(request, str(usr) + ' has been promoted as admin!')
    return redirect('classroom-settings', pk=pk)

@login_required
def remove_admin(request, pk, code):
    usr = User.objects.get(profile__id=code)
    clss = Class.objects.get(id=pk)
    if request.user == usr and clss.admin.count() == 1:
        msgs.warning(request, 'You cannot remove yourself if you are the only admin left. Transfer your admin access to other user and try again!')
        return redirect('classroom-settings', pk=pk)
    else:    
        clss.admin.remove(usr)
        clss.save()
        msgs.error(request, str(usr) + ' has been demoted to member')
    return redirect('classroom-settings', pk=pk)