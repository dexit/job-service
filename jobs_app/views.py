from rest_framework import generics
from rest_framework import permissions as drf_permissions
from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework import mixins

from simple_login import views as dsl_views

from jobs_app import models
from jobs_app import serializers
from jobs_app import permissions


def get_serializer_class(request):
    email = request.data.get('email', None)
    # If the user didn't provide email, just use default serializer.
    if not email:
        return serializers.UserSerializer
    try:
        # If user exists, check its type and return serializer accordingly.
        user = models.User.objects.get(email=email)
        if user.type == models.TYPE_ACCOUNT_COMPANY:
            return serializers.CompanySerializer
    except models.User.DoesNotExist:
        pass
    return serializers.UserSerializer


class Register(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer

    def get_serializer_class(self):
        account_type = int(self.request.data.get('type', 0))
        if not account_type:
            raise exceptions.ValidationError('Must provide "type" parameter.')
        if account_type == models.TYPE_ACCOUNT_COMPANY:
            return serializers.CompanySerializer
        elif account_type == models.TYPE_ACCOUNT_USER:
            return serializers.UserSerializer
        else:
            raise exceptions.ValidationError('Parameter "type" must be either 2 or 3.')


class Activate(dsl_views.ActivationAPIView):
    user_model = models.User

    def get_serializer_class(self):
        return get_serializer_class(self.request)


class ActivationKeyRequest(dsl_views.ActivationKeyRequestAPIView):
    user_model = models.User

    def get_serializer_class(self):
        return get_serializer_class(self.request)


class Login(dsl_views.LoginAPIView):
    user_model = models.User

    def get_serializer_class(self):
        return get_serializer_class(self.request)


class Profile(dsl_views.RetrieveUpdateDestroyProfileAPIView):
    user_model = models.User

    def get_serializer_class(self):
        if self.request.user.type == models.TYPE_ACCOUNT_COMPANY:
            return serializers.CompanySerializer
        return serializers.UserSerializer


class ForgotPassword(dsl_views.PasswordResetRequestAPIView):
    user_model = models.User


class ChangePassword(dsl_views.PasswordChangeAPIView):
    user_model = models.User


class Status(dsl_views.StatusAPIView):
    user_model = models.User


class ExperienceModelViewSet(viewsets.ModelViewSet):
    permission_classes = (drf_permissions.IsAuthenticated, )
    serializer_class = serializers.ExperienceSerializer

    def get_queryset(self):
        return models.Experience.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EducationModelViewSet(viewsets.ModelViewSet):
    permission_classes = (drf_permissions.IsAuthenticated, )
    serializer_class = serializers.EducationSerializer

    def get_queryset(self):
        return models.Education.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (drf_permissions.IsAuthenticated, permissions.IsCompany)
    serializer_class = serializers.JobSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        return models.JobPosting.objects.filter(creator=self.request.user)


class JobCategoryListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.JobCategorySerializer
    queryset = models.JobCategory.objects.all()


class JobLocationListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.JobLocationSerializer
    queryset = models.JobLocation.objects.all()


class PostingTypeListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.PostingTypeSerializer
    queryset = models.PostingType.objects.all()
