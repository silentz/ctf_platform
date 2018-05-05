from rest_framework import permissions
from api.models import Contest, Task
from django.utils import timezone


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class IsAdminOrTaskOpen(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            now = timezone.now()
            return now >= obj.contest.start_dattime and \
                (obj.contest.finish_datetime is None or now < obj.contest.finish_datetime)


class IsAdminOrParentTaskOpen(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            now = timezone.now()
            return now >= obj.task.contest.start_datetime and \
                (obj.task.contest.finish_datetime is None or now < obj.task.contest.finish_datetime)


class IsAdminOrContestOpen(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            now = timezone.now()
            return now >= obj.start_datetime and (obj.finish_datetime is None or now < obj.finish_datetime)
