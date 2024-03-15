from random import random
from typing import Type

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import RoomForm
from .models import MessageModel, RoomModel, TopicModel

UserModel: Type[User] = get_user_model()


# auth
def auth_login(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('all_rooms')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            UserModel.objects.get(username=username)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('all_rooms')
            else:
                raise Exception('')
        except (Exception,):
            messages.error(request, message='Username or Password does not exist.')

    context = {'page': page}
    return render(request, 'base_templates/login_register.html', context)


def auth_logout(request):
    logout(request)
    return redirect('all_rooms')


def auth_register(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username.lower()
            user.save()
            return redirect('auth_login')
        else:
            messages.error(request, 'Registration error.')

    context = {'page': page, 'form': form}
    return render(request, 'base_templates/login_register.html', context)


# rooms
def get_rooms(request):
    query = request.GET.get('q')
    user = request.user

    q = (Q(name__exact=query) |
         Q(name__icontains=query) |
         Q(topic__name__exact=query) |
         Q(description__icontains=query))

    if query and query != 'my_rooms':
        rooms = RoomModel.objects.filter(q)
    elif query == 'my_rooms':
        rooms = RoomModel.objects.filter(host_id=user)
    else:
        rooms = RoomModel.objects.all()

    topics = TopicModel.objects.all()
    room_count = rooms.count()
    room_messages = MessageModel.objects.filter(room__topic__name__exact=query)[:25] if query else MessageModel.objects.all()[:25]
    context = {'rooms': rooms, 'topics': topics, "room_count": room_count, 'room_messages': room_messages}
    return render(request, 'base_templates/rooms_page.html', context)


def get_room(request, pk):
    room = RoomModel.objects.get(id=pk)
    room_messages = room.messagemodel_set.all()
    participants = room.participants.all()
    print(participants)

    if request.method == "POST":
        MessageModel.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base_templates/room_page.html', context)


@login_required(login_url='/auth_login')
def create_room(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_rooms')

    context = {'form': form}
    return render(request, 'base_templates/room_form.html', context)


@login_required(login_url='/auth_login')
def update_room(request, pk):
    room = RoomModel.objects.get(id=pk)
    form = RoomForm(instance=room)

    if room.host != request.user and not request.user.is_superuser:
        messages.error('You are not allowed to update the room!')
        return None

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            cut = room.name.split('(Updated)')
            if len(cut) > 2:
                messages.error(message='No "(Updated)" in name of room!', request=request)
            elif len(cut) == 2:
                room.name = cut[0] + cut[1] + ' (Updated)'
                form.save()
                return redirect('all_rooms')
            else:
                room.name += ' (Updated)'
                form.save()
                return redirect('all_rooms')

    context = {'form': form}
    return render(request, 'base_templates/room_form.html', context)


@login_required(login_url='/auth_login')
def delete_room(request, pk):
    room = RoomModel.objects.get(id=pk)

    if room.host != request.user and not request.user.is_superuser:
        messages.error('You are not allowed to update the room!')
        return None

    if request.method == 'POST':
        room.delete()
        return redirect('all_rooms')
    context = {'item': room}
    return render(request, 'base_templates/delete.html', context)


# @login_required(login_url='/auth_login')
# def update_message(request, pk):
#     room_message = MessageModel.objects.get(id=pk)
#     form = RoomForm(instance=room)
#
#     if request.method == 'POST':
#         if room.host != request.user and not request.user.is_superuser:
#             messages.error('You are not allowed to update the room!')
#             return None
#
#         form = RoomForm(request.POST, instance=room)
#         if form.is_valid():
#             form.save()
#             return redirect('all_rooms')
#
#     context = {'form': form}
#     return render(request, 'base_templates/room_form.html', context)


@login_required(login_url='/auth_login')
def delete_message(request, pk):
    room_message = MessageModel.objects.get(id=pk)

    if request.user != room_message.user and not request.user.is_superuser:
        messages.error('You are not allowed to update the room!')
        return None

    if request.method == 'POST':
        room_message.delete()
        return redirect('room', pk=room_message.room.id)

    context = {'item': room_message}
    return render(request, 'base_templates/delete.html', context)

