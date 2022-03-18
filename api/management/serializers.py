from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from api.models import House, TypeHouse, User, Comment, Action, Rating, RentManage, Service
from api.house.serializers import HouseSerializer, TypeHouseSerializer
from api.user.serializers import UserSerializer
# from api.user.serializers import UserSerializer


class RentManageSerializer(ModelSerializer):
    # house_id = HouseSerializer()
    # created_by = UserSerializer()

    class Meta:
        model = RentManage
        fields = ["id", "house_id", "check_in_date", "check_out_date", "status", "created_date", "created_by", "totalPrice"]


class GetRentManageSerializer(ModelSerializer):
    house_id = HouseSerializer()
    created_by = UserSerializer()

    class Meta:
        model = RentManage
        fields = ["id", "house_id", "check_in_date", "check_out_date", "status", "created_date", "created_by"]


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class RentalHouseSerializer(ModelSerializer):
    created_by = UserSerializer()
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
        fields = ["id", "name", "image", "image1", "image2", "image3", "image4", "price", "updated_date", "type_house", "description", "bed", "guest", "bath_room", "bed_room", "address", "created_by"]


class RentalHouseManagementSerializer(ModelSerializer):
    house_id = HouseSerializer()
    created_by = UserSerializer()

    class Meta:
        model = RentManage
        fields = ["id", "house_id", "check_in_date", "check_out_date", "status", "created_date", "created_by", "totalPrice"]


class HouseForRentSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField()
    image3 = serializers.ImageField()
    image4 = serializers.ImageField()
    type_house_id = serializers.IntegerField()

    class Meta:
        model = House
        fields = ["id", "name", "image", "image1", "image2", "image3", "image4", "price", "type_house_id", "bed", "guest", "bath_room", "bed_room", "description", "address"]


class HouseUpdateSerializer(ModelSerializer):
    image = serializers.ImageField(required=False)
    image1 = serializers.ImageField(required=False)
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)
    image4 = serializers.ImageField(required=False)
    type_house_id = serializers.IntegerField(required=False)

    class Meta:
        model = House
        fields = ["id", "name", "image", "image1", "image2", "image3", "image4", "price", "type_house_id", "bed", "guest", "bath_room", "bed_room", "description", "address"]


class BookingManagementSerializer(ModelSerializer):
    house_id = HouseSerializer()
    created_by = UserSerializer()

    class Meta:
        model = RentManage
        fields = ["id", "house_id", "check_in_date", "check_out_date", "status", "created_date", "created_by", "totalPrice"]


class BookingUpdateSerializer(ModelSerializer):

    class Meta:
        model = RentManage
        fields = ["id", "status"]
