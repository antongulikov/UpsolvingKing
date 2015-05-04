from django.conf.urls import url, include
from views import mainPage

urlpatterns = [ url(r'^', mainPage)]
