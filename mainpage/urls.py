from django.conf.urls import url, include
from views import mainPage, lolPage

urlpatterns = [ url(r'^lol', lolPage), url(r'^', mainPage),
                ]
