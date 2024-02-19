from django.urls import path
from .views import get_rooms, get_room

urlpatterns = [
    path('', get_rooms),
    path('/<int:pk>', get_room, name='room')
]
