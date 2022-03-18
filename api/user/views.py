from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from api.models import HostRegister, House, TypeHouse, User, Comment, Action, Rating, RentManage
from .serializers import GetHostRegisterSerializer, HostRegisterSerializer, MySimpleJWTAdminSerializer, UserLevelSerializer, UserSerializer, MySimpleJWTSerializer, UserInfoSerializer, UserUpdateSerializer, UserAvatarSerializer, ChangePasswordSerializer
from django.conf import settings


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user', 'post']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(username=request.user.username).first()
            serializer = UserUpdateSerializer(data=request.data, context={'request': request}, instance=user)
            if serializer.is_valid():
                update = serializer.update(validated_data=request.data, instance=user)
                if update:
                    return Response({'status': 'successful', 'notification': 'Update successful!'}, status=status.HTTP_201_CREATED)
            return Response({'status': 'fail', 'notification': list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status': 'fail', 'notification': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=False, url_path="update-avatar")
    def update_avatar(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(user=request.user)
            serializer = UserAvatarSerializer(data=request.data, context={'request': request}, instance=user)
            if serializer.is_valid():
                update = serializer.update(validated_data=request.data, instance=user)
                if update:
                    return Response({'status': 'successful', 'notification': 'Update successful!'}, status=status.HTTP_201_CREATED)
            return Response({'status': 'fail', 'notification': list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status': 'fail', 'notification': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=True, url_path="update-level")
    def update_level(self, request, id_user):
        try:
            user = User.objects.get(id=id_user)
            user.level = 2
            user.save()
            return Response({'status': 'successful', 'notification': 'Update successful!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'status': 'fail', 'notification': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(viewsets.ViewSet, generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            print("check pass")
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MySimpleJWTSerializer

class MyTokenObtainPairViewAdmin(TokenObtainPairView):
    serializer_class = MySimpleJWTAdminSerializer

class HostRegisterViewSet(viewsets.ModelViewSet):
    # queryset = House.objects.filter(delete_flag=False)
    serializer_class = HostRegisterSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         return [permissions.AllowAny()]

    #     return [permissions.IsAuthenticated()]

    def get_queryset(self):
        hostRegister = HostRegister.objects.filter(delete_flag=False)

        q = self.request.query_params.get('q')
        if q is not None:
            hostRegister = hostRegister.filter(name__contains=q)

        return hostRegister

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        data = res.data
        obj = HostRegister.objects.get(id=data["id"])
        obj.created_by = request.user
        obj.save()
        return res

    @action(methods=['PUT'], detail=True, url_path="update-status-register")
    def update_status_register(self, request, id_register):
        try:
            host_register = HostRegister.objects.get(id=id_register)
            host_register.delete_flag = True
            host_register.save()
            return Response({'status': 'successful', 'notification': 'Update successful!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'status': 'fail', 'notification': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

class GetHostRegisterViewSet(viewsets.ModelViewSet):
    serializer_class = GetHostRegisterSerializer


    def list(self, request):
        queryset = HostRegister.objects.filter(delete_flag=False).order_by('-created_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response((serializer.data), status=status.HTTP_200_OK)
