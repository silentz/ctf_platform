from rest_framework import permissions
from api.models import Contest, Task
from django.utils import timezone
from django.shortcuts import get_object_or_404


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


class IsAdminOrParentContestAllowed(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            user_groups = request.user.groups.all()
            contest_groups = obj.contest.allowed_groups.all()
            return user_groups.intersection(contest_groups).count() > 0


class IsAdminOrParentContestOpen(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj.contest.training:
            return True
        else:
            now = timezone.now()
            return now >= obj.contest.start_datetime and now < obj.contest.finish_datetime


class IsAdminOrParentTaskAllowed(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            user_groups = request.user.groups.all()
            contest_groups = obj.task.contest.allowed_groups.all()
            return user_groups.intersection(contest_groups).count() > 0


class IsAdminOrParentTaskOpen(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj.task.contest.training:
            return True
        else:
            now = timezone.now()
            return now >= obj.task.contest.start_datetime and now < obj.task.contest.finish_datetime


class IsAdminOrContestAllowed(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            user_groups = request.user.groups.all()
            contest_groups = obj.allowed_groups.all()
            return user_groups.intersection(contest_groups).count() > 0


class IsAdminOrContestOpen(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj.training:
            return True
        else:
            now = timezone.now()
            return now >= obj.start_datetime and now < obj.finish_datetime


class IsAdminOrTargetContestAllowed(permissions.BasePermission):

    def has_permission(self, request, view):
        contest = get_object_or_404(Contest, id=request.query_params.get('for', None))
        if request.user.is_staff:
            return True
        else:
            user_groups = request.user.groups.all()
            contest_groups = contest.allowed_groups.all()
            return user_groups.intersection(contest_groups).count() > 0


class IsAdminOrTargetContestOpen(permissions.BasePermission):

    def has_permission(self, request, view):
        contest = get_object_or_404(Contest, id=request.query_params.get('for', None))
        if request.user.is_staff or contest.training:
            return True
        else:
            now = timezone.now()
            return now >= contest.start_datetime and now < contest.finish_datetime
