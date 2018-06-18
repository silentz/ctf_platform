from rest_framework import viewsets
from django.contrib.auth.models import User, Group, Permission
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


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return TaskAdminSerializer
        elif self.action == 'retrieve':
            return TaskSerializer
        else:
            raise PermissionDenied

    def get_permissions(self):
        if self.action == 'pass_flag':
            self.permission_classes = [IsAdminOrTaskNotHidden, IsAdminOrParentContestAllowed, IsAdminOrParentContestOpen, 
                                       IsAuthenticated]
        else:
            self.permission_classes = [IsAdminOrTaskNotHidden, IsAdminOrParentContestAllowed, IsAdminOrParentContestOpen,
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
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'bad'}, status=status.HTTP_400_BAD_REQUEST)


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

    def get_queryset(self):
        contest_id = self.request.query_params.get('for', None)
        if contest_id is None:
            return Message.objects.none()
        else:
            return Message.objects.filter(contest__id=contest_id)


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
            user_score = sum([entry.task.score for entry in TaskSolved.objects.filter(user=user)])
            result.append({'username': user.username, 'score': user_score})
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
            user_status = "admin" if request.user.is_staff else "user"
            return Response(
                {"status": user_status, "username": username},
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
        if serializer.is_valid() and password is not None:
            user = User(username=username)
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
