from django.db import models


class RoomModel(models.Model):
    class Meta:
        db_table = 'rooms_model'

    name = models.CharField(max_length=50)
    description = models.TextField(default='No_description', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
