from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import House, TypeHouse, User, Comment, Action, Rating, RentManage
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
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", "password", "avatar"]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class TypeHouseSerializer(ModelSerializer):
    class Meta:
        model = TypeHouse
        fields = ["id", "name"]


class HouseSerializer(ModelSerializer):
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
        fields = ["id", "name", "image", "price", "created_date", "type_house", "description"]


# class HouseDetailSerializer(HouseSerializer):
#     class Meta:
#         model = HouseSerializer.Meta.model
#         fields = HouseSerializer.Meta.fields + ['description']


class CommentSerializer(ModelSerializer):
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


class RentManageSerializer(ModelSerializer):
    # house_id = HouseSerializer()
    # created_by = UserSerializer()

    class Meta:
        model = RentManage
        fields = ["id", "house_id", "check_in_date", "check_out_date", "status", "created_date", "created_by"]


class GetRentManageSerializer(ModelSerializer):
    house_id = HouseSerializer()
    created_by = UserSerializer()

    class Meta:
        model = RentManage
        fields = ["id", "house_id", "check_in_date", "check_out_date", "status", "created_date", "created_by"]


