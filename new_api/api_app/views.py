from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework import permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from api_app.models import User
from api_app.serializers import UserSerizlizer
from api_app.permissions import IsLoogedInUserOrAdmin, IsAdminUser

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerizlizer
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
        



        