from rest_framework import serializers

from jobs_app import models


class ExperienceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.Experience.objects.all(), required=False)

    class Meta:
        model = models.Experience
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.Education.objects.all(), required=False)

    class Meta:
        model = models.Education
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(required=True)
    experience = ExperienceSerializer(read_only=True, many=True)
    education = EducationSerializer(read_only=True, many=True)

    class Meta:
        model = models.User
        fields = (
            'id',
            'email',
            'password',
            'full_name',
            'location',
            'photo',
            'phone_number',
            'skills',
            'experience',
            'education',
        )
