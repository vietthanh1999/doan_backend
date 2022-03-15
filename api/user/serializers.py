from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models import House, TypeHouse, User, Comment, Action, Rating, RentManage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class MySimpleJWTSerializer(TokenObtainPairSerializer):

    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #     user_obj = User.objects.get(username=user)
    #     #
    #     token['email'] = user_obj.email
    #     token['first_name'] = user_obj.first_name
    #     token['last_name'] = user_obj.last_name
    #
    # groups = Group.objects.filter(user=user_obj)
    # roles = ''
    # for g in groups:
    #     roles += g.name + ';'
    # token['roles'] = roles
    # return token

    def validate(self, attrs):
        print(attrs)
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        user_obj = User.objects.filter(username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)


class UserSerializer(ModelSerializer):
    level = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", "password", "avatar", 'level']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserInfoSerializer(ModelSerializer):

    avatar = SerializerMethodField()

    def get_avatar(self, user):
        print(self.context)
        request = self.context['request']
        name = user.avatar.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", "password", "avatar", 'level']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }


class UserUpdateSerializer(ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "avatar"]


class UserAvatarSerializer(ModelSerializer):

    class Meta:
        model = House
        fields = ["avatar"]


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
