from rest_framework import serializers
from .models import Reminder
from . import utils


class ReminderSerializer(utils.DateValidateMixin, serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Reminder
        exclude = ('reminded_count',)

    def validate_title(self, value):
        return value.lower()
