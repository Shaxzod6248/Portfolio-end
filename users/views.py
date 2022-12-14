from email import message
from django.dispatch.dispatcher import receiver
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import *
from django.contrib.auth.models import User

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 9)

    context = {'users': profiles,
               'search_query': search_query,
               'custom_range': custom_range}

    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    user = Profil.objects.get(id=pk)
    context = {
        "user": user
    }
    return render(request, 'users/profile.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')
        
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы вошли в систему!")
            return redirect('profiles')
        else:
            messages.error(request, 'Нет такого логина и пароля')


    return render(request, "users/login.html")

def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы!')
    return redirect('login')


def register_user(request):
    form = CustomUserCreationForm()
    for f in form:
        if f.label == "Password":
            f.label = "Пароль"
        elif f.label == "Password confirmation":
            f.label = "Подтвердить Пароль"

    context = {
        "form": form
    }

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)

            messages.success(request, "Пользователь зарегистрировался")
            return redirect('profiles')
        else:
            messages.error(request, form.errors)

    return render(request, "users/register.html", context)


@login_required(login_url='login')
def account(request):
    profil = request.user.profil
    context = {
        "profil": profil
    }
    print('profi', profil)
    print('profil.skill_set.all', profil.skill_set.all())

    return render(request, "users/account.html", context)



@login_required(login_url='login')
def account_edit(request):
    profil = request.user.profil
    form = ProfileForm(instance=profil)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        "form": form
    }
    return render(request,"users/account_edit.html", context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profil
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = profile
            skill.save()
            messages.success(request, 'Успешно!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profil
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Навык Добавлен')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profil
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Удалено!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


def inbox(request):
    print("inbox request.user", request.user)
    profile = request.user.profil

    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profil
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profil.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profil
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Сообщение доставлено!')
            return redirect('profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)