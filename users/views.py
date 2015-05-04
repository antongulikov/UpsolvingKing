from django.shortcuts import render
from django.http.response import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from users.models import UpUser

# Create your views here.

def userPage(request, username):
    try:
        args = {}
        user = UpUser.objects.get(username=username)
        args['problems'] = user.problem_set.all()
        args['user'] = user.username
        return render_to_response('userPage.html', args)
    except:
        return redirect('/')

