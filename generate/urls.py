from django.conf.urls import url, include
from views import generate

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', generate)
    ]

