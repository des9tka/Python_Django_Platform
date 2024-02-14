from django.shortcuts import render
from django.forms.models import model_to_dict

from django.http import HttpResponse

from .models import RoomModel


def get_rooms(request):
    rooms = RoomModel.objects.all()
    context = {'rooms': rooms}
    print(context)
    return render(request, 'rooms_templates/rooms_page.html', context)


def get_room(request, pk):
    room = RoomModel.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'rooms_templates/room_page.html', context)
