from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models import House, TypeHouse, User, Comment, Action, Rating, RentManage, Message
from api.user.serializers import UserSerializer, UserInfoSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MessageSerializer(ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Message
        fields = ["id", "content", "created_date", "created_by", "send_to",]


class ChatListSerializer(ModelSerializer):
    created_by = UserSerializer()
    send_to = UserSerializer()

    class Meta:
        model = Message
        fields = ["id", "created_date", "send_to", "created_by"]
