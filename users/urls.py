from django.conf.urls import url, include
from views import userPage, userProblem

urlpatterns = [
            url(r'(?P<username>[\w.@+-]+)/problems/page/(?P<page_number>[\d+]+)/$', userProblem),
            url(r'(?P<username>[\w.@+-]+)/problems/$', userProblem),
            url(r'(?P<username>[\w.@+-]+)', userPage)
                ]
