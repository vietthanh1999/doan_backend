from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from api.models import RentManage, House, Message
from .serializers import MessageSerializer, ChatListSerializer
from django.conf import settings
from django.shortcuts import render
from django.db.models import Q
from api.pusher import pusher_client


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/rooms.html', {
        'room_name': room_name
    })


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.all()

    @action(methods=["get"], detail=False, url_path="get_message", url_name="get_message")
    def get_message(self, request, *args, **kwargs):
        try:
            queryset = Message.objects.filter(chat_room=kwargs.get("chat_id"))

            serializer = MessageSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception Message ViewSet: ", e)
            return Response({"data": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False, url_path="get_chat_list", url_name="get_chat_list")
    def get_chat_list(self, request, *args, **kwargs):
        try:
            queryset = Message.objects.all().distinct('send_to', 'created_by')

            serializer = ChatListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception Message ViewSet: ", e)
            return Response({"data": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


class MessageAPIView(APIView):
    def post(self, request):
        pusher_client.trigger('chat', 'message', {
            'username': request.data['username'],
            'message': request.data['message']
        })

        return Response([])

