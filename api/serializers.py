from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'id', 'url')

    def create(self, validated_data):
        user = User(username=validated_data.get('username'))
        user.set_password(validated_data.get('password'))
        user.save()
        return user
