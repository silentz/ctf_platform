from rest_framework import permissions
from api.models import Contest, Task
from datetime import datetime


class IsAdminOrReadOnly(permissions.BasePermission):

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
            now = datetime.now()
            return now >= obj.contest.start_time and \
                (obj.contest.finish_time is None or now < obj.contest.finish_time)


class IsAdminOrParentTaskOpen(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            now = datetime.now()
            return now >= obj.task.contest.start_time and \
                (obj.task.contest.finish_time is None or now < obj.task.contest.finish_time)


class IsAdminOrContestOpen(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            now = datetime.now()
            return now >= obj.start_time and (obj.finish_time is None or now < obj.finish_time)
