from django.db import models

from simple_login import models as dsl_models

TYPE_ACCOUNT_ADMIN = 1
TYPE_ACCOUNT_USER = 2
TYPE_ACCOUNT_COMPANY = 3

ACCOUNT_CHOICES = (
    (TYPE_ACCOUNT_ADMIN, 'Admin'),
    (TYPE_ACCOUNT_USER, 'User'),
    (TYPE_ACCOUNT_COMPANY, 'Company'),
)

JOB_TYPE_CHOICES = (
    ('Full-time', 'Full-time'),
    ('Part-time', 'Part-time'),
    ('Internship', 'Internship')
)
JOB_LANGUAGE_TYPE = (
    ('English', 'English'),
    ('Malay', 'Malay'),
    ('Chinese', 'Chinese')
)


class User(dsl_models.BaseUser):
    account_activation_sms_otp = None
    password_reset_sms_otp = None

    type = models.IntegerField(default=TYPE_ACCOUNT_ADMIN, choices=ACCOUNT_CHOICES, blank=False)
    name = models.CharField(max_length=255, blank=True)


class UserDetail(models.Model):
    user = models.OneToOneField(User, related_name='user_details')
    location = models.CharField(max_length=64, blank=True)
    photo = models.ImageField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=64, blank=True)


class CompanyDetail(models.Model):
    user = models.OneToOneField(User, related_name='company_details')
    type = models.CharField(max_length=128, blank=True)
    details = models.CharField(max_length=300, blank=True)
    contact_number = models.CharField(max_length=64, blank=True)
    website = models.URLField(blank=True)
    registration_number = models.CharField(max_length=255, blank=False)


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


class JobLocation(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name_plural = 'Job categories'

    def __str__(self):
        return self.name


class PostingType(models.Model):
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.description


class JobPosting(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, blank=False)
    type = models.CharField(max_length=16, blank=False, choices=JOB_TYPE_CHOICES)
    location = models.ForeignKey(JobLocation, blank=False)
    categories = models.ManyToManyField(JobCategory, blank=False)
    scope = models.CharField(max_length=255, blank=False)
    requirement = models.CharField(max_length=1024, blank=False)
    detailed_description = models.CharField(max_length=2048, blank=False)
    salary = models.CharField(max_length=16, blank=True)
    posting_type = models.ForeignKey(PostingType, blank=False)
    language = models.CharField(max_length=16, blank=False, choices=JOB_LANGUAGE_TYPE)
