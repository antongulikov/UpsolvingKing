from django.shortcuts import render
from django.http.response import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from users.models import UpUser, UserTag
from django.core.paginator import Paginator
from django.core.context_processors import csrf
from random import shuffle

# Create your views here.

def showStat(request, username):
    args = {}
    args.update(csrf(request))
    try:
        user = UpUser.objects.get(username=username)
        tags = UserTag.objects.filter(user=user)
        tags = sorted(tags, key = lambda x : -x.power)
        args['user'] = user.username
        N = 7
        if request.POST:
            try:
                N = int(request.POST.get('cnt','7'))
            except:
                pass
        if N < 0:
            N = 7
        tags = tags[:N]
        args['tags'] = tags

        return render_to_response('userStat.html', args)
    except:
        return redirect('/qwe')

def userProblem(request, username, page_number = 1):
    try:
        args = {}
        user = UpUser.objects.get(username=username)
        args['user'] = user.username
        all_problems = user.problem_set.all()
        all_problems = sorted(all_problems, key = lambda x : x.id)
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

