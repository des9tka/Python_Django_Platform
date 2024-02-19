from django.contrib import admin

from .models import RoomModel, TopicModel, MessageModel


admin.site.register(RoomModel)
admin.site.register(TopicModel)
admin.site.register(MessageModel)
