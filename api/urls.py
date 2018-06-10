from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('contests', views.ContestViewSet, base_name='contest')
router.register('files', views.TaskFileViewSet)
router.register('groups', views.GroupViewSet)
router.register('permissions', views.PermissionViewSet)
router.register('tasks', views.TaskViewSet)
router.register('users', views.UserViewSet)
router.register('hints', views.HintViewSet)
router.register('messages', views.MessageViewSet)
router.register('news', views.NewsViewSet)

urlpatterns = [
    *router.urls,
    path('auth/login/', views.UserLoginAPIView.as_view(), name='login'),
    path('auth/register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('auth/logout/', views.UserLogoutAPIView.as_view(), name='logout'),
    path('auth/status/', views.UserStatusView.as_view(), name='status'),
    path('scoreboard/', views.ScoreboardView.as_view(), name='scoreboard'),
]
