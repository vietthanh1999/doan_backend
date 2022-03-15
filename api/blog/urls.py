
from django.urls import path, include, re_path
from . import views
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('blogs', views.BlogViewSet, 'blogs')

urlpatterns = [
    path('', include(router.urls)),
]
