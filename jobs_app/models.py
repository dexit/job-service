from django.db import models

from simple_login.models import BaseUser


class User(BaseUser):
    account_activation_sms_otp = None
    password_reset_sms_otp = None

    full_name = models.CharField(max_length=255, blank=False)
    location = models.CharField(max_length=64, blank=False)
    photo = models.ImageField(blank=True)
    skills = models.CharField(max_length=255, blank=False)


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experience')
    period = models.CharField(max_length=128, blank=False)
    title = models.CharField(max_length=128, blank=False)
    company = models.CharField(max_length=128, blank=False)


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    period = models.CharField(max_length=128, blank=False)
    qualification = models.CharField(max_length=128, blank=False)
    school = models.CharField(max_length=128, blank=False)
