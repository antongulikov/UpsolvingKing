from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Examples:
    # url(r'^$', 'upking.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),
    url(r'auth/', include('loginsys.urls')),
    url(r'profile/', include('users.urls')),
    url(r'^', include('mainpage.urls'))
]
