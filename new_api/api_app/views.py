from functools import partial
from django.conf import settings
from django.db.models import fields
from django.db.models.query import QuerySet
from django.http import request
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, viewsets, filters
from rest_framework import permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api_app.models import User, DocumentRequest
from api_app.serializers import (
    UserSerializer,
    DocumentRequestSerializer,
    DocumentReceivedSerializer,
)
from api_app.permissions import IsLoogedInUserOrAdmin, IsAdminUser
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "create":
            permission_classes = [AllowAny]
        elif (
            self.action == "retrieve"
            or self.action == "update"
            or self.action == "partial_update"
            or self.action == "list"
        ):
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


# class DocumentRequestViewSet(viewsets.ModelViewSet):
#     queryset = DocumentRequest.objects.all()
#     serializer_class = DocumentRequestSerializer


#     def perform_create(self, serializer):
#         serializer.save(from_user=self.request.user, status_request=DocumentRequest.INITIATED_STATUS)


class DocumentRequestListAPIView(generics.ListAPIView):
    queryset = DocumentRequest.objects.select_related("from_user").all()
    serializer_class = DocumentRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status_request"]
    ordering_fields = ["time"]
    ordering = ["time"]


class DocumentRequestCreateAPIView(generics.CreateAPIView):
    serializer_class = DocumentRequestSerializer
      
    def perform_create(self, serializer):
        serializer.save(
        from_user=self.request.user, status_request=DocumentRequest.INITIATED_STATUS
            )
            
        
        
    

class SentDocumentRequestListAPIView(generics.ListAPIView):
    serializer_class = DocumentRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["to_user"]
    ordering_fields = ["time"]
    ordering = ["time"]

    def get_queryset(self):
        user = self.request.user
        return DocumentRequest.objects.select_related("from_user").filter(
            from_user=user, status_request=DocumentRequest.INITIATED_STATUS
        )


class RepliedDocumentRequestListAPIView(generics.ListAPIView):
    serializer_class = DocumentReceivedSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["to_user"]
    ordering_fields = ["time"]
    ordering = ["time"]

    def get_queryset(self):
        user = self.request.user
        return DocumentRequest.objects.filter(
            from_user=user, status_request=DocumentRequest.RECEIVED_STATUS
        )


class ReceivedDocumentRequestListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DocumentReceivedSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["to_user"]
    ordering_fields = ["time"]
    ordering = ["time"]

    def get_queryset(self):
        user = self.request.user
        return DocumentRequest.objects.filter(to_user=user)

    def perform_create(self, serializer):
        serializer.save(
            from_user=self.request.user, status_request=DocumentRequest.RECEIVED_STATUS
        )
