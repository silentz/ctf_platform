from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('contests', views.ContestViewSet)
router.register('files', views.TaskFileViewSet)
router.register('groups', views.GroupViewSet)
router.register('permissions', views.PermissionViewSet)
router.register('tasks', views.TaskViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    *router.urls,
    path('auth/login/', views.UserLoginAPIView.as_view(), name='login'),
    path('auth/register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('auth/logout/', views.UserLogoutAPIView.as_view(), name='logout'),
]
