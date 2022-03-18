from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    level = models.IntegerField(default=3)
    phone_number = models.CharField(max_length=16, blank=True, null=True)

class TypeHouse(models.Model):
    name = models.CharField(max_length=200, null=False, unique=True)
    delete_flag = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class ItemBase(models.Model):
    class Meta:
        abstract = True

    delete_flag = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class HostRegister(ItemBase):
    before_identification = models.ImageField(upload_to='identification/%Y/%m', default=None)
    after_identification = models.ImageField(upload_to='identification/%Y/%m', default=None)
    description = models.TextField(null=True, blank=True)

class House(ItemBase):
    class Meta:
        ordering = ["-id"]

    name = models.CharField(max_length=200, null=False, unique=True)
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to='houses/%Y/%m', default=None)
    image1 = models.ImageField(upload_to='houses/%Y/%m', default=None)
    image2 = models.ImageField(upload_to='houses/%Y/%m', default=None)
    image3 = models.ImageField(upload_to='houses/%Y/%m', default=None)
    image4 = models.ImageField(upload_to='houses/%Y/%m', default=None)
    type_house = models.ForeignKey(TypeHouse, related_name='type_house', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bed = models.IntegerField(default=0)
    guest = models.IntegerField(default=0)
    bath_room = models.IntegerField(default=0)
    bed_room = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Service(ItemBase):
    house = models.OneToOneField(House, on_delete=models.CASCADE, primary_key=True)
    hairdryer = models.BooleanField(default=False, null=True, blank=True)
    shampoo = models.BooleanField(default=False, null=True, blank=True)
    hot_water = models.BooleanField(default=False, null=True, blank=True)
    clothes_dryer = models.BooleanField(default=False, null=True, blank=True)
    essential_amenities = models.BooleanField(default=False, null=True, blank=True)
    clothes_hangers = models.BooleanField(default=False, null=True, blank=True)
    iron = models.BooleanField(default=False, null=True, blank=True)
    television = models.BooleanField(default=False, null=True, blank=True)
    suitable_events = models.BooleanField(default=False, null=True, blank=True)
    air_conditioner = models.BooleanField(default=False, null=True, blank=True)
    fire_extinguisher = models.BooleanField(default=False, null=True, blank=True)
    wifi = models.BooleanField(default=False, null=True, blank=True)
    free_parking_property = models.BooleanField(default=False, null=True, blank=True)
    pool = models.BooleanField(default=False, null=True, blank=True)
    allow_smoking = models.BooleanField(default=False, null=True, blank=True)
    self_check_in = models.BooleanField(default=False, null=True, blank=True)
    door_staff = models.BooleanField(default=False, null=True, blank=True)
    long_term_stay_allowed = models.BooleanField(default=False, null=True, blank=True)
    indoor_security_camera = models.BooleanField(default=False, null=True, blank=True)
    kitchen = models.BooleanField(default=False, null=True, blank=True)
    washing_machine = models.BooleanField(default=False, null=True, blank=True)
    smoke_alarms = models.BooleanField(default=False, null=True, blank=True)
    co_gas_detector = models.BooleanField(default=False, null=True, blank=True)
    private_entrance = models.BooleanField(default=False, null=True, blank=True)
    heating_system = models.BooleanField(default=False, null=True, blank=True)


class Comment(models.Model):
    content = models.TextField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class ActionBase(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Action(ActionBase):
    LIKE, UNLIKE = range(2)
    ACTIONS = [
        (LIKE, 'like'),
        (UNLIKE, 'unlike')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)


class Rating(ActionBase):
    rate = models.PositiveSmallIntegerField(default=0)


class RentManage(ItemBase):
    house_id = models.ForeignKey(House, related_name='rent_house', on_delete=models.SET_NULL, blank=True, null=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        ordering = ['created_date']


class Message(models.Model):
    created_by = models.ForeignKey(User, related_name='created_by_messages', on_delete=models.CASCADE)
    send_to = models.ForeignKey(User, related_name='send_to_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.created_by.username


class Blog(ItemBase):
    class Meta:
        ordering = ["-id"]

    name = models.CharField(max_length=200, null=False, unique=True)
    image = models.ImageField(upload_to='blog/%Y/%m', default=None)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
