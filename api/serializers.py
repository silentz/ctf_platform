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
    inside = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'invite_code', 'inside')

    def get_invite_code(self, obj):
        return obj.options.invite_code

    def get_inside(self, obj):
        return self.context['request'].user.groups.filter(id=obj.id).exists()


class GroupSerializer(serializers.ModelSerializer):
    inside = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'inside')

    def get_inside(self, obj):
        return self.context['request'].user.groups.filter(id=obj.id).exists()


class ContestListSerializer(serializers.ModelSerializer):
    allowed_groups_names = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = ('id', 'name', 'start_datetime', 'finish_datetime',
                  'allowed_groups', 'allowed_groups_names')

    def get_allowed_groups_names(self, obj):
        return [group.name for group in obj.allowed_groups.all()]


class ContestSerializer(serializers.ModelSerializer):
    allowed_groups_names = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = ('id', 'name', 'start_datetime', 'training', 'finish_datetime',
                  'tasks', 'allowed_groups', 'messages', 'allowed_groups_names')

    def get_allowed_groups_names(self, obj):
        return [group.name for group in obj.allowed_groups.all()]


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
    category_name = serializers.SerializerMethodField()
    solved = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'score', 'description', 'contest',
                  'category', 'files', 'hints', 'category_name', 'solved')

    def get_category_name(self, obj):
        return obj.category.name

    def get_solved(self, obj):
        user = self.context['request'].user
        return TaskSolved.objects.filter(user=user, task=obj).exists()


class TaskAdminSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    solved = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'score', 'description', 'contest', 'category',
                  'files', 'flag', 'hints', 'category_name', 'solved')

    def get_category_name(self, obj):
        return obj.category.name

    def get_solved(self, obj):
        user = self.context['request'].user
        return TaskSolved.objects.filter(user=user, task=obj).exists()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'contest', 'text', 'time')


class HintListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = ('id', 'task')


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = ('id', 'task', 'text')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'text', 'time')
