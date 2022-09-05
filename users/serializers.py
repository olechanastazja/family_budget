from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        # Hash the user's password.
        user.set_password(validated_data['password'])
        user.save()
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
