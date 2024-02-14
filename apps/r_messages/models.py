from typing import Type

from django.db import models

from apps.rooms.models import RoomModel

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# from apps.users.models import UserModel as User

UserModel: Type[User] = get_user_model()


class MessageModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

