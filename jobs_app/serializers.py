from rest_framework import serializers

from jobs_app import models


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
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.filter(type=models.TYPE_ACCOUNT_COMPANY), required=False,
        write_only=True)

    class Meta:
        model = models.CompanyDetail
        fields = ('type', 'details', 'contact_number', 'website', 'registration_number', 'user')


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
        if user_details:
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
    password = serializers.CharField(write_only=True)
    type = serializers.IntegerField(required=True)
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
        for k, v in company_details.items():
            setattr(existing_details, k, v)
        existing_details.save()
        return instance


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPosting
        fields = '__all__'


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
