from rest_framework import serializers
from users.models import Profile, CustomUser
from reminder.models import Reminder


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    reminders = serializers.PrimaryKeyRelatedField(many=True,
      queryset=Reminder.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'reminders']
