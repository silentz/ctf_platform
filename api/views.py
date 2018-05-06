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
    permission_classes = (IsAdminOrTaskOpen, IsAdminOrReadOnly, IsAuthenticated)
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return TaskAdminSerializer
        elif self.action == 'retrieve':
            return TaskSerializer
        else:
            raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(TaskViewSet, self).dispatch(request, *args, **kwargs)

    @action(methods=['post'], detail=True)
    def pass_flag(self, request, pk):
        obj = self.get_object()
        if obj.check_flag(request.data.get('flag', None)):
            obj.solved.add(request.user)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'bad'}, status=status.HTTP_200_OK)


class ContestViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, IsAdminOrContestOpen, IsAuthenticated)
    queryset = Contest.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ContestListSerializer
        else:
            return ContestSerializer


class TaskFileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrParentTaskOpen, IsAdminOrReadOnly, IsAuthenticated)
    queryset = TaskFile.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskFileCreateSerializer
        else:
            return TaskFileSerializer

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(TaskFileViewSet, self).dispatch(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def download(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(instance.file, chunk_size))
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = "attachment; filename=%s" % instance.name
        return response


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FlagViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser, IsAuthenticated)
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permissions = (IsAdminOrReadOnly, IsAuthenticated)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permissions = (IsAdminOrReadOnly, IsAuthenticated)


class UserLogoutAPIView(APIView):

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
