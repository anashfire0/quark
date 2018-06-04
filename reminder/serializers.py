from rest_framework import serializers
from .models import Reminder
from . import utils


class ReminderSerializer(utils.SlugValidateMixin,utils.DateValidateMixin, serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'

    def validate_title(self, value):
        return value.lower()

