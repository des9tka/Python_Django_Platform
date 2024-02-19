from typing import Type

from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# from apps.users.models import default_user

UserModel: Type[User] = get_user_model()


class TopicModel(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


# def default_topic():
#     TopicModel.objects.get(name='Just Chatting')


class RoomModel(models.Model):
    class Meta:
        db_table = 'rooms_model'

    name = models.CharField(max_length=50)
    host = models.ForeignKey(UserModel, on_delete=models.SET_NULL, default=None, null=True)
    topic = models.ForeignKey(TopicModel, on_delete=models.SET_NULL, default=None, null=True)
    description = models.TextField(blank=True, default=None, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MessageModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:15]
