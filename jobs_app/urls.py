from django.conf.urls import url
from rest_framework import routers

from jobs_app import views

from jobs_app.views import (
    ActivationKeyRequest,
    ForgotPassword,
    ChangePassword,
    Register,
    Login,
    Activate,
    Profile,
    Status
)

url_router = routers.DefaultRouter()
url_router.register(r'api/experience', views.ExperienceListCreateAPIView, base_name='experiences')
url_router.register(r'api/education', views.EducationListCreateAPIView, base_name='education')

urlpatterns = [
    url(r'^api/register$', Register.as_view()),
    url(r'^api/request-activation-key$', ActivationKeyRequest.as_view()),
    url(r'^api/activate$', Activate.as_view()),
    url(r'^api/login$', Login.as_view()),
    url(r'^api/forgot-password$', ForgotPassword.as_view()),
    url(r'^api/change-password$', ChangePassword.as_view()),
    url(r'^api/status$', Status.as_view()),
    url(r'^api/me$', Profile.as_view()),
]

urlpatterns += url_router.urls
