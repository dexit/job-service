from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
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
url_router.register(r'api/experience', views.ExperienceModelViewSet, base_name='experiences')
url_router.register(r'api/education', views.EducationModelViewSet, base_name='education')
url_router.register(r'api/post-job', views.JobListCreateAPIView, base_name='jobs')
url_router.register(r'api/jobs/locations', views.JobLocationListView, base_name='locations')
url_router.register(r'api/jobs/categories', views.JobCategoryListView, base_name='categories')
url_router.register(r'api/jobs/types', views.PostingTypeListView, base_name='types')
url_router.register(r'api/jobs/saved', views.SavedJobListCreateAPIView, base_name='saved')

urlpatterns = [
    url(r'^api/register$', Register.as_view(), name='register'),
    url(r'^api/request-activation-key$', ActivationKeyRequest.as_view()),
    url(r'^api/activate$', Activate.as_view()),
    url(r'^api/login$', Login.as_view()),
    url(r'^api/forgot-password$', ForgotPassword.as_view()),
    url(r'^api/change-password$', ChangePassword.as_view()),
    url(r'^api/status$', Status.as_view()),
    url(r'^api/me$', Profile.as_view()),
    url(r'^api/jobs/$', views.JobFilterAPIView.as_view()),
    url(r'^api/jobs/(?P<pk>[0-9]+)$', views.JobView.as_view()),
    url(r'^api/messages/$', views.MessageListCreateAPIView.as_view()),
    url(r'^api/messages/metadata$', views.MessageMetadataAPIView.as_view()),
    url(r'^api/pushkey$', views.PushKeyCreateAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += url_router.urls
