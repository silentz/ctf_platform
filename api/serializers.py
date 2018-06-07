from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from api.models import *
from api.permissions import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'groups')


class GroupCreateSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(max_length=512)

    class Meta:
        model = Group
        fields = ('id', 'name', 'invite_code')


class GroupAdminSerializer(serializers.ModelSerializer):
    invite_code = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'invite_code')

    def get_invite_code(self, obj):
        return obj.options.invite_code


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'url')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name',)


class ContestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'name', 'start_datetime', 'finish_datetime', 'allowed_groups')


class ContestSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = ('id', 'name', 'start_datetime', 'finish_datetime',
                  'tasks', 'allowed_groups', 'messages', 'categories')

    def get_categories(self, obj):
        result = set([task.category.id for task in obj.tasks.all()])
        return list(result)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskFileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ('id', 'file', 'task')

    def create(self, validated_data):
        name = validated_data['file'].name
        file = validated_data['file']
        task = validated_data['task']
        return TaskFile.objects.create(task=task, name=name, file=file)


class TaskFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ('id', 'url',)


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ('id', 'task', 'name')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'score', 'description', 'contest', 'category', 'files', 'hints')


class TaskAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'score', 'description', 'contest', 'category', 'files', 'flag', 'hints')


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'contest')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'contest', 'text')


class HintListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = ('id', 'task')


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = ('id', 'task', 'text')
