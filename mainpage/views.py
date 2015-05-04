from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.contrib import auth
from django.shortcuts import render_to_response


# Create your views here.

def mainPage(request):
    return render_to_response('mainPage.html', {'user': auth.get_user(request).username})


