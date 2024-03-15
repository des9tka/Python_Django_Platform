from django.urls import path

from .views import create_room, delete_message, delete_room, get_room, get_rooms, update_room

urlpatterns = [
    path('', get_rooms, name='all_rooms'),
    path('/<int:pk>', get_room, name='room'),
    path('/create', create_room, name='create_room'),
    path('/update/<int:pk>', update_room, name='update_room'),
    path('/delete/<int:pk>', delete_room, name='delete_room'),
    path('/message/delete/<int:pk>', delete_message, name='delete_message')
]
