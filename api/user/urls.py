
from django.urls import path, include, re_path
from . import views
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, 'users')

user = UserViewSet.as_view({
    'put': 'update',
})

update_avatar = UserViewSet.as_view({
    'put': 'update_avatar',
})

change_password = ChangePasswordView.as_view({
    'put': 'update',
})

urlpatterns = [
    path('', include(router.urls)),
    path("user/update", user, name="user-update"),
    path("user/update-avatar", update_avatar, name="avatar-update"),
    path("user/change-password", change_password, name="change-password"),
]
