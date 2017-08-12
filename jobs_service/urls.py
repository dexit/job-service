from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from jobs_app import views
from jobs_app import urls

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(urls)),
    url(r'^register-company/$', views.register, name='register-company'),
    url(r'^company-profile/$', views.CompanyProfile.as_view(), name='company-profile'),
    url(r'^post-ad/$', views.PostAd.as_view(), name='post-ad'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='site/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]
