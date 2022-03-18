from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Count

from api.models import RentManage, House
from .serializers import RentManageSerializer, GetRentManageSerializer, RentalHouseManagementSerializer, RentalHouseSerializer, HouseForRentSerializer, HouseUpdateSerializer, BookingManagementSerializer, BookingUpdateSerializer
from django.conf import settings


class RentalHouseViewSet(viewsets.ModelViewSet):
    serializer_class = RentalHouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = House.objects.filter(delete_flag=False, created_by__username=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RentManageViewSet(viewsets.ModelViewSet):
    queryset = RentManage.objects.filter(delete_flag=False)
    serializer_class = RentManageSerializer
    # permission_classes = [permissions.IsAuthenticated]


# Danh sách đặt phòng của renter
class RentalHouseManagementViewSet(viewsets.ModelViewSet):
    queryset = RentManage.objects.filter(delete_flag=False)
    serializer_class = RentalHouseManagementSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request):

        queryset = RentManage.objects.filter(created_by__username=request.user).order_by('-updated_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True, url_path="update-status", url_name="get-detail-house")
    # /houses/{pk}/get_detail_house
    def get_detail_house(self, request, pk):
        try:
            h = House.objects.get(pk=pk)
        except House.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=RentalHouseSerializer(h).data, status=status.HTTP_200_OK)


class GetRentManageViewSet(viewsets.ModelViewSet):
    queryset = RentManage.objects.filter(delete_flag=False)
    serializer_class = GetRentManageSerializer

    def list(self, request):
        queryset = RentManage.objects.filter(house_id__created_by__username=request.user).order_by('-created_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Quản lý nhà cho thuê (host)
class HouseForRentViewSet(viewsets.ModelViewSet):
    queryset = House.objects.filter(delete_flag=False)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HouseForRentSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        data = res.data
        obj = House.objects.get(id=data["id"])
        obj.created_by = request.user
        obj.save()
        return res

    def update(self, request, public_id, *args, **kwargs):
        try:
            house = House.objects.filter(id=public_id, delete_flag=False).first()
            serializer = HouseUpdateSerializer(data=request.data, context={'request': request}, instance=house)
            print(request.data)
            if serializer.is_valid():
                update = serializer.update(validated_data=request.data, instance=house)
                if update:
                    return Response({'status': 'successful', 'notification': 'Update successful!'}, status=status.HTTP_201_CREATED)
            return Response({'status': 'fail', 'notification': list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status': 'fail', 'notification': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            obj = House.objects.get(id=kwargs.get("public_id"))
            obj.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"data": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["PUT"], detail=False, url_path="public_video", url_name="public_video"
    )
    def public_video(self, request, *args, **kwargs):
        try:
            obj = House.objects.get(id=kwargs.get("public_id"))
            is_delete = request.data["delete_flag"]
            obj.delete_flag = is_delete
            obj.save()
            return Response(
                {"message": "Update success!"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print("Public House: ", e)
            pass
        return Response({"data": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


# Quản lý đặt nhà của host
class BookingManagementViewSet(viewsets.ModelViewSet):
    queryset = RentManage.objects.filter(delete_flag=False)
    serializer_class = BookingManagementSerializer

    def list(self, request):
        if request.user.level != 1:
            queryset = RentManage.objects.filter(house_id__created_by=request.user).order_by('-created_date')
        else:
            queryset = RentManage.objects.all().order_by('-created_date')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, public_id, *args, **kwargs):
        try:
            house = RentManage.objects.filter(id=public_id, delete_flag=False).first()
            house.status = True
            house.save()
            return Response({'status': 'successful', 'notification': 'Update successful!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'status': 'fail', 'notification': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            obj = RentManage.objects.get(id=kwargs.get("public_id"))
            obj.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"data": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False, url_path="get-income-statistics", url_name="get-income-statistics")
    def get_income_statistics(self, request):
        try:
            income_list = []
            for i in range(1, 13):
                income_list.append({
                    "month": i,
                    "income": 0
                })

            rent_list = RentManage.objects.filter(house_id__created_by=request.user).order_by('-created_date')

            for rent in rent_list:
                income_list[rent.check_in_date.month - 1]['income'] += rent.totalPrice

        except RentManage.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({
                "results": income_list
            })

    @action(methods=["get"], detail=False, url_path="get-income-statistics", url_name="get-income-statistics")
    def get_info_doughnut(self, request):
        try:
            income_list = []

            rent_list = RentManage.objects.filter(house_id__created_by=request.user).values('house_id', 'house_id__name').annotate(dcount=Count('house_id'))
            print(rent_list)
            for rent in rent_list:
                income_list.append(rent)

        except RentManage.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({
            "results": income_list
        })

        # return Response(data=JsonResponse(a), status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True, url_path="check-comment", url_name="check-comment")
    def check_comment(self, request, house_id):
        try:
            checkComment = False

            rent_list = RentManage.objects.filter(created_by=request.user, house_id=house_id)
            if (len(rent_list) > 0):
                checkComment = True

        except RentManage.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({
            "results": checkComment
        })
