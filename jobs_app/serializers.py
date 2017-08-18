from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework import exceptions

from jobs_app import models


class RichPrimaryKeyRelatedField(serializers.RelatedField):
    # Taken from: https://gist.github.com/AndrewIngram/5c79a3e99ccd20245613
    default_error_messages = serializers.PrimaryKeyRelatedField.default_error_messages

    def __init__(self, serializer, **kwargs):
        self.many = kwargs.get('many', False)
        self.serializer = serializer
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        return self.serializer(value, many=self.many).data


class ExperienceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.filter(type=models.TYPE_ACCOUNT_USER), required=False,
        write_only=True)

    class Meta:
        model = models.Experience
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.filter(type=models.TYPE_ACCOUNT_USER), required=False,
        write_only=True)

    class Meta:
        model = models.Education
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.filter(type=models.TYPE_ACCOUNT_USER), required=False,
        write_only=True)

    class Meta:
        model = models.UserDetail
        fields = ('location', 'photo', 'skills', 'user', 'contact_number')


class CompanyDetailSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    # user = serializers.PrimaryKeyRelatedField(
    #     queryset=models.User.objects.filter(type=models.TYPE_ACCOUNT_COMPANY), required=False,
    #     write_only=True)

    class Meta:
        model = models.CompanyDetail
        fields = ('type', 'details', 'contact_number', 'website', 'registration_number', 'photo')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    type = serializers.IntegerField(required=True)
    user_details = UserDetailSerializer(required=False)
    experience = ExperienceSerializer(required=False, many=True)
    education = EducationSerializer(required=False, many=True)

    class Meta:
        model = models.User
        fields = ('id', 'type', 'email', 'name', 'password', 'user_details', 'experience',
                  'education')

    def validate_user_details(self, user_details):
        validator = UserDetailSerializer(data=user_details)
        validator.is_valid(raise_exception=True)
        return user_details

    def validate_experience(self, experience):
        validator = ExperienceSerializer(data=experience, many=True)
        validator.is_valid(raise_exception=True)
        return experience

    def validate_education(self, education):
        validator = EducationSerializer(data=education, many=True)
        validator.is_valid(raise_exception=True)
        return education

    def create(self, validated_data):
        experience = validated_data.pop('experience', {})
        education = validated_data.pop('education', {})
        user_details = validated_data.pop('user_details', {})
        user = models.User.objects.create(**validated_data)
        models.UserDetail.objects.create(user=user, **user_details)
        for exp in experience:
            models.Experience.objects.create(user=user, **exp)
        for edu in education:
            models.Education.objects.create(user=user, **edu)
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        experience = validated_data.pop('experience', {})
        education = validated_data.pop('education', {})
        user_details = validated_data.pop('user_details', {})
        existing_details = models.UserDetail.objects.get(user=instance)
        for k, v in user_details.items():
            setattr(existing_details, k, v)
        existing_details.save()
        for exp in experience:
            models.Experience.objects.create(user=instance, **exp)
        for edu in education:
            models.Education.objects.create(user=instance, **edu)
        return instance


class CompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    type = serializers.ChoiceField(choices=((3, "Company"), (3, "Company")), required=True)
    company_details = CompanyDetailSerializer(required=True)

    class Meta:
        model = models.User
        fields = ('id', 'type', 'email', 'name', 'password', 'company_details')

    def validate_company_details(self, company_details):
        validator = CompanyDetailSerializer(data=company_details)
        validator.is_valid(raise_exception=True)
        return company_details

    def create(self, validated_data):
        company_details = validated_data.pop('company_details', {})
        user = models.User.objects.create(**validated_data)
        if company_details:
            models.CompanyDetail.objects.create(user=user, **company_details)
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        company_details = validated_data.pop('company_details', {})
        existing_details = models.CompanyDetail.objects.get(user=instance)
        print(company_details)
        for k, v in company_details.items():
            setattr(existing_details, k, v)
        existing_details.save()
        return instance


class JobSerializer(serializers.ModelSerializer):
    qrcode = serializers.ImageField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    creator_name = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = models.JobPosting
        fields = '__all__'

    def validate_type(self, job_type):
        types = ['full-time', 'part-time', 'internship']
        if job_type.lower() not in ['full-time', 'part-time', 'internship']:
            raise exceptions.ValidationError('type must be one of {}'.format(', '.join(types)))
        return job_type

    def get_creator_name(self, obj):
        return obj.creator.name

    def get_location_name(self, obj):
        return obj.location.name

    def get_company_logo(self, obj):
        company = models.CompanyDetail.objects.get(user=obj.creator)
        return company.photo.url if company.photo else None


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobCategory
        fields = '__all__'


class JobLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobLocation
        fields = '__all__'


class PostingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostingType
        fields = '__all__'


class SavedJobSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=models.JobPosting.objects.all())

    class Meta:
        model = models.SavedJob
        fields = '__all__'


class PushKeySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all(), required=False)

    class Meta:
        model = models.PushKey
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all(), required=False)

    class Meta:
        model = models.Message
        fields = '__all__'


class MessageToValidator(serializers.Serializer):
    to = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all(), required=True)


class MessageFilterValidator(serializers.Serializer):
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all(), required=True)
