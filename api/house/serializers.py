from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models import House, TypeHouse, User, Comment, Action, Rating, RentManage
from api.user.serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from api.user.serializers import UserSerializer, UserInfoSerializer


class TypeHouseSerializer(ModelSerializer):
    name = serializers.CharField(required=False)
    class Meta:
        model = TypeHouse
        fields = ["id", "name", "delete_flag"]


class HouseSerializer(ModelSerializer):
    created_by = UserInfoSerializer()
    type_house = TypeHouseSerializer()
    image = SerializerMethodField()

    def get_image(self, house):
        request = self.context['request']
        name = house.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = House
        fields = ["id", "name", "image", "price", "created_date", "type_house", "bed", "guest", "bath_room", "bed_room", "address", "description", "created_by"]


class CommentSerializer(ModelSerializer):
    creator = UserInfoSerializer()

    class Meta:
        model = Comment
        fields = ["id", "content", "creator", "created_date", "updated_date"]


class AddCommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "content", "created_date", "updated_date"]


class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "type", "created_date"]


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "rate", "created_date"]
