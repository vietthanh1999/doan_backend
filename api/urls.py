
from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import re_path, include


router = DefaultRouter()

# router.register('houses', views.HouseViewSet, 'house')
# router.register('type-house', views.TypeHouseViewSet, 'type-house')
# router.register('users', views.UserViewSet, 'user')
# router.register('comments', views.CommentViewSet, 'comment')
# router.register('rent-manage', views.RentManageViewSet, 'rent-manage')
# router.register('get-rent-manage', views.GetRentManageViewSet, 'get-rent-manage')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('api.management.urls')),
    path('', include('api.user.urls')),
    path('', include('api.house.urls')),
    path('', include('api.chat.urls')),
    path('', include('api.blog.urls')),
    re_path(r'^auth/login/$', views.MyTokenObtainPairView.as_view()),
]
