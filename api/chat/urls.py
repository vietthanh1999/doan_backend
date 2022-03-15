from django.urls import path, include, re_path
from . import views
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# app_name = 'chat'
get_message = MessageViewSet.as_view({"get": "get_message"})
get_chat_list = MessageViewSet.as_view({"get": "get_chat_list"})

chat = MessageAPIView.as_view()

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', views.index, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path("get-message/<str:chat_id>", get_message, name="get-message"),
    path("get-chat-list/", get_chat_list, name="get-chat-list"),
    path('mess/', MessageAPIView.as_view())
]
