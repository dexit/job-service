from django.conf.urls import include, url
from django.contrib import admin

from jobs_app import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(urls)),
]
