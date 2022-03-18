
from django.urls import path, include, re_path
from . import views
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, 'users')
router.register('host-register', views.HostRegisterViewSet, 'host-register')

user = UserViewSet.as_view({
    'put': 'update',
})

update_avatar = UserViewSet.as_view({
    'put': 'update_avatar',
})

update_level = UserViewSet.as_view({
    'put': 'update_level',
})


change_password = ChangePasswordView.as_view({
    'put': 'update',
})

list_register_host = GetHostRegisterViewSet.as_view({
    'get': 'list',
})

update_status_register = HostRegisterViewSet.as_view({
    'put': 'update_status_register',
})

urlpatterns = [
    path('', include(router.urls)),
    path("user/update", user, name="user-update"),
    path("user/update-avatar", update_avatar, name="avatar-update"),
    path("user/update-level/<str:id_user>", update_level, name="update-level"),
    path("user/change-password", change_password, name="change-password"),
    path("list-register-host/", list_register_host, name="list-register-host"),
    path("update-status-register/<str:id_register>", update_status_register, name="update-status-register"),
    re_path(r'^auth/login-admin/$', views.MyTokenObtainPairViewAdmin.as_view()),
]
