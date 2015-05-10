from django.conf.urls import url, include
from views import login, logout, updateInf

urlpatterns = [ url(r'^login', login),
                url(r'^logout', logout),
                url(r'^', updateInf)]
