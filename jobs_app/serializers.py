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
    experience = ExperienceSerializer(required=False, many=True)
    education = EducationSerializer(required=False, many=True)

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

    def create(self, validated_data):
        experience = validated_data.pop('experience', {})
        education = validated_data.pop('education', {})
        user = models.User.objects.create(**validated_data)
        for exp in experience:
            models.Experience.objects.create(user=user, **exp)
        for edu in education:
            models.Education.objects.create(user=user, **edu)
        return user

    def update(self, instance, validated_data):
        experience = validated_data.pop('experience', {})
        education = validated_data.pop('education', {})
        for exp in experience:
            models.Experience.objects.create(user=instance, **exp)
        for edu in education:
            models.Education.objects.create(user=instance, **edu)
        return instance
