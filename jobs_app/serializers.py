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
        user = models.User.objects.create(**validated_data)
        for exp in experience:
            models.Experience.objects.create(user=user, **exp)
        for edu in education:
            models.Education.objects.create(user=user, **edu)
        return user

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.location = validated_data.get('location', instance.location)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.skills = validated_data.get('skills', instance.skills)
        instance.save()
        experience = validated_data.pop('experience', {})
        education = validated_data.pop('education', {})
        for exp in experience:
            models.Experience.objects.create(user=instance, **exp)
        for edu in education:
            models.Education.objects.create(user=instance, **edu)
        return instance
