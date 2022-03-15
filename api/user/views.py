from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from api.models import House, TypeHouse, User, Comment, Action, Rating, RentManage
from .serializers import UserSerializer, MySimpleJWTSerializer, UserInfoSerializer, UserUpdateSerializer, UserAvatarSerializer, ChangePasswordSerializer
from django.conf import settings


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView, generics.ListAPIView):
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
            print(request.data)
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
