from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from api.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions


class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


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
            return Response({'status': 'not authed'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            login(request, user)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
