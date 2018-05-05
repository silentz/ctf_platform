from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from api.models import *
from api.permissions import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'url', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ('url', 'name',)


class ContestListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contest
        fields = ('url', 'name', 'start_datetime', 'finish_datetime', 'allowed_groups')


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contest
        fields = ('url', 'name', 'start_datetime', 'finish_datetime', 'tasks', 'allowed_groups')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FlagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Flag
        fields = '__all__'


class TaskFileCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskFile
        fields = ('url', 'file', 'task')

    def create(self, validated_data):
        name = validated_data['file'].name
        file = validated_data['file']
        task = validated_data['task']
        return TaskFile.objects.create(task=task, name=name, file=file)


class TaskFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskFile
        fields = ('url', 'task', 'name')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('url', 'name', 'score', 'description', 'contest', 'category',
                  'solved', 'use_generator', 'files')


class TaskAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('url', 'name', 'score', 'description', 'contest', 'category',
                  'solved', 'use_generator', 'files', 'token', 'flag', 'generator_flags')
