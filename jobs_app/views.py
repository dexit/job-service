from rest_framework import generics
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import viewsets

from simple_login import views

from jobs_app import models
from jobs_app import serializers


class Register(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class Activate(views.ActivationAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class ActivationKeyRequest(views.ActivationKeyRequestAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class Login(views.LoginAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class Profile(views.RetrieveUpdateDestroyProfileAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class ForgotPassword(views.PasswordResetRequestAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class ChangePassword(views.PasswordChangeAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class Status(views.StatusAPIView):
    user_model = models.User
    serializer_class = serializers.UserSerializer


class ExperienceListCreateAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.ExperienceSerializer

    def get_queryset(self):
        return models.Experience.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EducationListCreateAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.EducationSerializer

    def get_queryset(self):
        return models.Education.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
