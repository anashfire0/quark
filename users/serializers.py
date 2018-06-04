from rest_framework import serializers
from users.models import Profile, CustomUser
from reminder.models import Reminder


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # reminders = serializers.PrimaryKeyRelatedField(many=True,
      # queryset=Reminder.objects.all())

    reminders = serializers.HyperlinkedIdentityField(many=True,
        view_name="reminder:reminder_detail_rest", read_only=True)
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'reminders']
