from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models import House, TypeHouse, User, Comment, Action, Rating, RentManage, Blog
from api.user.serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from api.user.serializers import UserSerializer, UserInfoSerializer


class BlogSerializer(ModelSerializer):
    created_by = UserInfoSerializer(required=False)

    class Meta:
        model = Blog
        fields = ["id", "name", "image", "created_date", "description", "created_by"]


class BlogListSerializer(ModelSerializer):
    created_by = UserInfoSerializer(required=False)
    image = SerializerMethodField()

    def get_image(self, blog):
        request = self.context['request']
        name = blog.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = Blog
        fields = ["id", "name", "image", "created_date", "description", "created_by"]
