from django.conf.urls import url

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
