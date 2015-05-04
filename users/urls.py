from django.conf.urls import url, include
from views import userPage

urlpatterns = [ url(r'(?P<username>[\w.@+-]+)', userPage)]
