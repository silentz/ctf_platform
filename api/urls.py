from django.urls import path, include
from api.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, base_name='user')

urlpatterns = [
    *router.urls,
]
