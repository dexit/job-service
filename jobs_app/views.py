from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions as drf_permissions
from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework import response
from rest_framework import status
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django import shortcuts

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
        account_type = int(self.request.data.get('type', 3))
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
        return Response({'serializer': serializers.CompanySerializer()})

    def post(self, request):
        data = request.data.dict()
        name = {}
        company_details = {}
        for item in data:
            print(item)
            if item.startswith('company_details'):
                pass
        serializer = serializers.CompanySerializer(data=request.data)
        serializer.is_valid()
        print(serializer.validated_data)
        print(serializer.data)
        serializer.save()
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
        serializer.save(creator=self.request.user)
        return Response({'serializer': serializer})


class JobFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(name='categories__name', lookup_expr='contains')
    location = django_filters.CharFilter(name='location__name')
    type = django_filters.CharFilter()

    class Meta:
        model = models.JobPosting
        fields = ('categories', 'type', 'location')


class JobFilterAPIView(generics.ListAPIView):
    serializer_class = serializers.JobSerializer
    queryset = models.JobPosting.objects.all().order_by('-created_at')
    filter_class = JobFilter


class JobView(generics.RetrieveAPIView):
    serializer_class = serializers.JobSerializer

    def get_object(self):
        return shortcuts.get_object_or_404(models.JobPosting, id=int(self.kwargs['pk']))


class SavedJobListCreateAPIView(mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = (drf_permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'DELETE':
            return serializers.JobSerializer
        return serializers.SavedJobSerializer

    def get_queryset(self):
        return models.JobPosting.objects.filter(
            id__in=[job.job.id for job in models.SavedJob.objects.filter(saver=self.request.user)]
        )

    def perform_create(self, serializer):
        serializer.save(saver=self.request.user)

    def get_object(self):
        return shortcuts.get_object_or_404(models.SavedJob, id=self.kwargs['pk'])


class MessageListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (drf_permissions.IsAuthenticated, )
    serializer_class = serializers.MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def post(self, request, *args, **kwargs):
        to_validator = serializers.MessageToValidator(data=self.request.data)
        to_validator.is_valid(True)
        if self.request.user.type == models.TYPE_ACCOUNT_COMPANY:
            self.request.data.update({'company': self.request.user.id})
            self.request.data.update({'user': to_validator.validated_data['to'].id})
        elif self.request.user.type == models.TYPE_ACCOUNT_USER:
            self.request.data.update({'user': self.request.user.id})
            self.request.data.update({'company': to_validator.validated_data['to'].id})
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        to_validator = serializers.MessageToValidator(data=self.request.data)
        to_validator.is_valid(True)
        return models.Message.objects.filter(sender=self.request.user,
                                             receiver=to_validator.validated_data['to'])


class MessageMetadataAPIView(APIView):
    permission_classes = (drf_permissions.IsAuthenticated,)

    def get(self, *args, **kwargs):
        seen = set()
        messages_with_unique_profile = []
        if self.request.user.type == models.TYPE_ACCOUNT_COMPANY:
            all_messages = models.Message.objects.filter(company=self.request.user)
            for message in all_messages:
                if message.user not in seen:
                    messages_with_unique_profile.append(message)
                    seen.add(message.user)
        else:
            all_messages = models.Message.objects.filter(user=self.request.user)
            for message in all_messages:
                if message.company not in seen:
                    messages_with_unique_profile.append(message)
                    seen.add(message.company)

        data = []
        for message in messages_with_unique_profile:
            msg_data = {'latest_text': message.text}
            if self.request.user.type == models.TYPE_ACCOUNT_COMPANY:
                user = models.UserDetail.objects.get(user=message.user)
                msg_data.update({
                    'unread_count': all_messages.filter(
                        ~Q(creator=self.request.user), company=self.request.user,
                        user=message.user, read=False).count()})
            else:
                user = models.CompanyDetail.objects.get(user=message.user)
                msg_data.update({
                    'unread_count': all_messages.filter(
                        ~Q(creator=self.request.user), company=message.company,
                        user=self.request.user, read=False).count()})
            msg_data.update({
                'user_id': user.user.id,
                'photo_url': user.photo.url if user.photo else "",
                'full_name': user.user.name,
                'created_at': message.created_at.__str__(),
            })
            data.append(msg_data)
        return response.Response(data=data, status=status.HTTP_200_OK)


class PushKeyCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.PushKeySerializer
    permission_classes = (drf_permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        self.request.data.update({'user': self.request.user.id})
        device = self.request.data.get('device')
        if not device:
            return Response(data={'device': 'required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            device_push_key = models.PushKey.objects.get(device=device)
            serializer = serializers.PushKeySerializer(
                data=self.request.data, instance=device_push_key, partial=True)
            serializer.is_valid(True)
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        except models.PushKey.DoesNotExist:
            return super().post(request, *args, **kwargs)


def register(request):
    template = loader.get_template("site/register.html")
    return HttpResponse(template.render(request=request))
