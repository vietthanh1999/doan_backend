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
from .serializers import HouseSerializer, TypeHouseSerializer, CommentSerializer, RatingSerializer, ActionSerializer, AddCommentSerializer
from django.conf import settings


class HouseViewSet(viewsets.ModelViewSet):
    # queryset = House.objects.filter(delete_flag=False)
    serializer_class = HouseSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_detail_house']:
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        houses = House.objects.filter(delete_flag=False)

        q = self.request.query_params.get('q')
        if q is not None:
            houses = houses.filter(name__contains=q)

        type_house = self.request.query_params.get('type_house')
        if type_house is not None:
            houses = houses.filter(type_house=type_house)

        return houses

    @action(methods=["post"], detail=True, url_path="hide-house", url_name="hide-house")
    # /houses/{pk}/hide_house
    def hide_house(self, request, pk):
        try:
            h = House.objects.get(pk=pk)
            h.delete_flag = True
            h.save()
        except House.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=HouseSerializer(h, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True, url_path="get-detail-house", url_name="get-detail-house")
    # /houses/{pk}/get_detail_house
    def get_detail_house(self, request, pk):
        try:
            h = House.objects.get(pk=pk)
        except House.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=HouseSerializer(h).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content=content, house=self.get_object(), creator=request.user)

            return Response(AddCommentSerializer(c).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path="like")
    def take_action(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except IndexError or ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            a = Action.objects.create(type=action_type, creator=request.user, house=self.get_object())

            return Response(ActionSerializer(a).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path="rating")
    def rate(self, request, pk):
        try:
            rating = int(request.data['rate'])
        except IndexError or ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rating.objects.create(rate=rating, creator=request.user, house=self.get_object())

            return Response(RatingSerializer(r).data, status=status.HTTP_200_OK)


class TypeHouseViewSet(viewsets.ModelViewSet):
    queryset = TypeHouse.objects.filter(delete_flag=False)
    serializer_class = TypeHouseSerializer


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permissions = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=True, url_path="get-list-comment")
    def get_list_comment(self, request, pk):

        queryset = Comment.objects.filter(house=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
