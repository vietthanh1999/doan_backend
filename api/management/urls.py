
from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
rental_house_management_list = RentalHouseManagementViewSet.as_view({
    'get': 'list',
})

rental_house_list = RentalHouseViewSet.as_view({
    'get': 'list'
})

house = HouseForRentViewSet.as_view({"post": "create"})
house_detail = HouseForRentViewSet.as_view({
    'put': 'update',
    'delete': 'destroy'
})

booking_management = BookingManagementViewSet.as_view({
    'get': 'list'
})

booking_update = BookingManagementViewSet.as_view({
    'put': 'update',
    'delete': 'destroy'
})

income_statistics = BookingManagementViewSet.as_view({
    'get': 'get_income_statistics'
})

get_info_doughnut = BookingManagementViewSet.as_view({
    'get': 'get_info_doughnut'
})

check_comment = BookingManagementViewSet.as_view({
    'get': 'check_comment'
})

router.register('get-rent-manage', views.GetRentManageViewSet, 'get-rent-manage')
# router.register('house-for-rent', views.HouseForRentViewSet, 'house-for-rent')
router.register('rent-manage', views.RentManageViewSet, 'rent-manage')

urlpatterns = [
    path('', include(router.urls)),
    path("house-for-rent/", house, name="house-for-rent"),
    path("house-update/<str:public_id>", house_detail, name="house-update"),

    path('rental-house-management-list/', rental_house_management_list, name='rental-house-management-list'),
    path('host/rental-house-list/', rental_house_list, name='rental-house-list'),

    path('host/booking-management/', booking_management, name='booking-management'),
    path('host/booking-management/<str:public_id>', booking_update, name='booking-update'),

    path('host/income-statistics/', income_statistics, name='income-statistics'),
    path('host/info_doughnut/', get_info_doughnut, name='info_doughnut'),
    path('check-comment/<str:house_id>', check_comment, name='check-comment'),

]
