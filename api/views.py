from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from api.models import *
from api.permissions import *
from api.serializers import *
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# registration setting
from django.conf import settings

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    channel_layer = get_channel_layer()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return TaskAdminSerializer
        elif self.action == 'retrieve':
            return TaskSerializer
        else:
            raise PermissionDenied

    def get_permissions(self):
        if self.action == 'pass_flag':
            self.permission_classes = [IsAdminOrTaskNotHidden, IsAdminOrParentContestAllowed,
                                       IsAdminOrParentContestOpen,
                                       IsAuthenticated]
        else:
            self.permission_classes = [IsAdminOrTaskNotHidden, IsAdminOrParentContestAllowed,
                                       IsAdminOrParentContestOpen,
                                       IsAdminOrReadOnly, IsAuthenticated]
        return super(TaskViewSet, self).get_permissions()

    @action(methods=['get'], detail=False)
    def solved(self, request):
        result = [entry.task for entry in request.user.solved_tasks.all()]
        serialized = TaskSerializer(result, context={'request': request}, many=True).data
        return Response(serialized, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def pass_flag(self, request, pk):
        obj = self.get_object()
        if obj.check_flag(request.data.get('flag', None)):
            TaskSolved.objects.get_or_create(task=obj, user=request.user)
            async_to_sync(self.channel_layer.group_send)(
                "scoreboard",
                {'type': 'scoreboard.changed'}
            )
            async_to_sync(self.channel_layer.group_send)(
                "contest_{}_scoreboard".format(obj.contest.id),
                {'type': 'scoreboard.changed'}
            )
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'bad'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def scoreboard(self, request, pk, *args, **kwargs):
        entries = TaskSolved.objects.filter(task=self.get_object()).order_by("time")
        result = [{'username': entry.user.username, 'time': entry.time} for entry in entries]
        return Response(result, status=status.HTTP_200_OK)


class ContestViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrContestAllowed, IsAdminOrReadOnly, IsAdminOrContestOpen, IsAuthenticated)

    def get_serializer_class(self):
        if self.action == 'list':
            return ContestListSerializer
        else:
            return ContestSerializer

    def get_queryset(self):
        if self.action == 'list':
            if self.request.query_params.get('training', None) == 'true':
                return Contest.objects.filter(training=True).all()
            else:
                return Contest.objects.filter(training=False).all()
        else:
            return Contest.objects.all()

    def is_permitted(self, request, obj):
        for permission in self.permission_classes:
            if not permission().has_object_permission(request, self, obj):
                return False
        return True

    def list(self, request):
        queryset = Contest.objects.filter(training=(request.query_params.get('training', None) == 'true'))
        contests = [contest for contest in queryset if self.is_permitted(request, contest)]
        serializer = ContestListSerializer(contests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def scoreboard(self, request, pk, *args, **kwargs):
        return Response(self.get_object().scoreboard(), status=status.HTTP_200_OK)


class TaskFileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrParentTaskAllowed, IsAdminOrParentTaskOpen, IsAdminOrReadOnly, IsAuthenticated)
    queryset = TaskFile.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskFileCreateSerializer
        elif self.action == 'list':
            return TaskFileListSerializer
        else:
            return TaskFileSerializer

    @action(methods=['get'], detail=True)
    def download(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(instance.file, chunk_size))
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = "attachment; filename=%s" % instance.name
        return response


class HintViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrParentTaskAllowed, IsAdminOrParentTaskOpen, IsAdminOrReadOnly, IsAuthenticated)
    queryset = Hint.objects.all()
    serializer_class = HintSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return HintListSerializer
        else:
            return HintSerializer


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrTargetContestAllowed, IsAdminOrTargetContestOpen, IsAdminOrParentContestOpen,
                          IsAdminOrReadOnly, IsAuthenticated)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    channel_layer = get_channel_layer()

    def call_update(self, contest_id, notify=None):
        contest_group = "contest_{}_notifications".format(contest_id)
        async_to_sync(self.channel_layer.group_send)(contest_group, {
            'type': 'notifications.changed',
            'data': notify
        })

    def get_queryset(self):
        contest_id = self.request.query_params.get('for', None)
        if contest_id is None:
            return Message.objects.none()
        else:
            return Message.objects.filter(contest__id=contest_id)
    
    def create(self, request, *args, **kwargs):
        self.call_update(request.data['contest'], notify=request.data['text'])
        return super(MessageViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.call_update(request.data['contest'])
        return super(MessageViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.call_update(self.get_object().contest.id)
        return super(MessageViewSet, self).destroy(request, *args, **kwargs)


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()

    def get_permissions(self):
        if self.action == 'access':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
        return super(GroupViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return GroupCreateSerializer
        elif self.request.user.is_staff:
            return GroupAdminSerializer
        else:
            return GroupSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        invite_code = request.data.get('invite_code', None)
        if Group.objects.filter(name=name).exists():
            return Response({'status': 'group already exists'}, status=status.HTTP_400_BAD_REQUEST)
        group = Group.objects.create(name=name)
        GroupAdditional.objects.create(group=group, invite_code=invite_code)
        serialized = GroupAdminSerializer(group, context={'request': request}).data
        return Response(serialized, status=status.HTTP_201_CREATED)

    def update(self, request, pk, partial=False):
        invite_code = request.data.get('invite_code', None)
        if invite_code is not None:
            options = self.get_object().options
            options.invite_code = invite_code
            options.save()
        return super(GroupViewSet, self).update(request, pk, partial)

    @action(methods=['post'], detail=True)
    def access(self, request, pk, *args, **kwargs):
        invite_code = request.data.get('invite_code', None)
        group = self.get_object()
        if invite_code == group.options.invite_code:
            request.user.groups.add(group)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'wrong invite code'}, status=status.HTTP_403_FORBIDDEN)


class ScoreboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        users = set([entry.user for entry in TaskSolved.objects.all()])
        result = []
        for user in users:
            obj = TaskSolved.objects.filter(user=user)
            user_score = sum([entry.task.score for entry in obj])
            last_accepted = max([int(entry.time.timestamp()) for entry in obj])
            result.append({
                'username': user.username,
                'full_name': user.last_name,
                'score': user_score,
                "last_accepted": last_accepted
            })
        result = sorted(result, key=lambda x: (-x['score'], x['last_accepted']))
        return Response(result, status=status.HTTP_200_OK)


class UserStatusView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if request.user.is_anonymous:
            return Response(
                {"status": "anonymous", "username": ""},
                status=status.HTTP_200_OK
            )
        else:
            username = request.user.username
            full_name = request.user.last_name
            user_status = "admin" if request.user.is_staff else "user"
            return Response(
                {"status": user_status, "username": username, "full_name": full_name},
                status=status.HTTP_200_OK
            )


class UserPasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)

        if request.user.check_password(old_password) and new_password is not None:
            request.user.set_password(new_password)
            request.user.save()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'bad'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        logout(request)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class UserRegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        full_name = request.data.get('full_name', None)
        if not settings.ALLOW_REGISTRATION:
            return Response({"status": "blocked"}, status=status.HTTP_400_BAD_REQUEST)
        elif serializer.is_valid() and (password is not None):
            user = User(username=username, last_name=full_name)
            user.set_password(password)
            user.save()
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'bad'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'status': 'bad'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            login(request, user)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
