from rest_framework import serializers
from .models import Reminder
from . import utils


class ReminderSerializer(utils.DateValidateMixin, serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.HyperlinkedIdentityField(view_name="reminder:reminder_detail_rest")

    class Meta:
        model = Reminder
        exclude = ('reminded_count',)

    def validate_title(self, value):
        return value.lower()
