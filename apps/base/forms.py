from django.forms import ModelForm
from .models import RoomModel


class RoomForm(ModelForm):
    class Meta:
        model = RoomModel
        fields = '__all__'
