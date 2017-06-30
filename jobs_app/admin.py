from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

from jobs_app import models


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = models.User


class JobLocationAdmin(admin.ModelAdmin):
    class Meta:
        model = models.JobLocation


class JobCategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = models.JobCategory


class PostingTypeAdmin(admin.ModelAdmin):
    class Meta:
        model = models.PostingType


admin.site.unregister(Group)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.JobLocation, JobLocationAdmin)
admin.site.register(models.JobCategory, JobCategoryAdmin)
admin.site.register(models.PostingType, PostingTypeAdmin)
