from django.shortcuts import render
from django.http.response import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from users.models import UpUser, UserTag
from django.core.paginator import Paginator

# Create your views here.

def showStat(request, username):
    try:
        user = UpUser.objects.get(username=username)
        tags = UserTag.objects.filter(user=user)
        tags = sorted(tags, key = lambda x : -x.power)
        args = {}
        args['user'] = user.username
        args['tags'] = tags[:10]
        return render_to_response('userStat.html', args)
    except:
        return redirect('/')

def userProblem(request, username, page_number = 1):
    try:
        args = {}
        user = UpUser.objects.get(username=username)
        args['user'] = user.username
        all_problems = user.problem_set.all()
        current_page = Paginator(all_problems, 20)
        args['problems'] = current_page.page(page_number)
        return render_to_response('problemsPage.html', args)
    except:
        return redirect('/')

def userPage(request, username):
    try:
        args = {}
        user = UpUser.objects.get(username=username)
        args['user'] = user.username
        return render_to_response('userPage.html', args)
    except:
        return redirect('/')

