from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Dog, UserPref


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        UserPref.objects.create(user=user)
        return user

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPref
        exclude = ['user']


class DogSerializer(serializers.ModelSerializer):
    added_by = serializers.ReadOnlyField(source='added_by.id')
    image_filename = serializers.SerializerMethodField()
    age = serializers.IntegerField(
        min_value=0,
        error_messages={
            'min_value': 'The Vulcan Science Directorate has determined that '
                         'time travel is impossible. Your dog cannot have a '
                         'negative age.'
        })

    class Meta:
        model = Dog
        exclude = ['_age', 'birthdate']

    def get_image_filename(self, instance):
        return instance.image_filename
