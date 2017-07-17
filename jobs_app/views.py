from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions as drf_permissions
from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response

import django_filters
from simple_login import views as dsl_views

from jobs_app import models
from jobs_app import serializers
from jobs_app import permissions
from jobs_app import forms


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


def company_login_view(request):
    if request.method == 'POST':
        form = forms.CompanyLoginForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/register-company/')
    else:
        form = forms.CompanyLoginForm()
    return render(request, 'registration/login.html', {'form': form})


class RegisterCompany(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register_company.html'

    def get(self, request):
        serializer = serializers.CompanySerializer()
        return Response({'serializer': serializers.CompanySerializer()})

    def post(self, request):
        serializer = serializers.CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'serializer': serializer})


class CompanyProfile(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'company_profile.html'

    def get(self, request):
        serializer = serializers.CompanySerializer(instance=request.user)
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = serializers.CompanySerializer(
            instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'serializer': serializer, 'profile': request.user})


class PostAd(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_ad.html'

    def get(self, request):
        return Response({'serializer': serializers.JobSerializer()})

    def post(self, request):
        serializer = serializers.JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'serializer': serializer})


class JobFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        name='categories__name',
        lookup_expr='contains',
    )
    location = django_filters.CharFilter(name='location__name')
    type = django_filters.CharFilter()

    class Meta:
        model = models.JobPosting
        fields = ('categories', 'type', 'location')


class JobFilterAPIView(generics.ListAPIView):
    serializer_class = serializers.JobSerializer
    queryset = models.JobPosting.objects.all().order_by('-created_at')
    filter_class = JobFilter
