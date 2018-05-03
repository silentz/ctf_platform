from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, base_name='user')

urlpatterns = [
    *router.urls,
    path('auth/login/', views.UserLoginAPIView.as_view(), name='login'),
    path('auth/register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('auth/logout/', views.UserLogoutAPIView.as_view(), name='logout'),
]
