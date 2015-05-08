from django.conf.urls import url, include
from views import userPage, userProblem

urlpatterns = [
            url(r'(?P<username>[\w.@+-]+)/problems/(\d*)', userProblem),
            url(r'(?P<username>[\w.@+-]+)', userPage)
                ]
