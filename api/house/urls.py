
from django.urls import path, include, re_path
from . import views
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('houses', views.HouseViewSet, 'houses')
router.register('type-house', views.TypeHouseViewSet, 'type-house')
router.register('comments', views.CommentViewSet, 'comment')

comment_house = CommentViewSet.as_view({
    'get': 'get_list_comment'
})

urlpatterns = [
    path('', include(router.urls)),
    path('house/list-comment/<str:pk>', comment_house, name='comment-house'),
]
