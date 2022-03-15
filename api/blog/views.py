from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from api.models import House, TypeHouse, User, Comment, Action, Rating, RentManage, Blog
from .serializers import BlogSerializer
from django.conf import settings


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        data = res.data

        obj = Blog.objects.get(id=data["id"])
        obj.created_by = request.user
        obj.save()
        return res

    def list(self, request):
        queryset = Blog.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
