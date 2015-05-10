from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin', include(admin.site.urls)),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^profile/', include('users.urls')),
    url(r'^generate/', include('generate.urls')),
    url(r'^', include('mainpage.urls'))
]
