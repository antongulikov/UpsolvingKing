import requests
import json
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from users.models import UpUser, Problem
from helpscript.additon import update_user_tag_relationship


def logout(request):
    auth.logout(request)
    return redirect('/')

def update_user(username, rating):
    user = ""
    if (len(UpUser.objects.filter(username=username)) > 0):
        user = UpUser.objects.get(username=username)
        user.rating = rating
        user.save()
    else:
        user = UpUser(username=username, rating=rating)
        user.save()
    q = requests.get('http://www.codeforces.com/api/user.status?handle={}&from=1&count=10000000'.format(username))
    q = q.text
    data = json.loads(q)
    current_watched = user.watched
    if data['status'] == 'OK':
        size_of_current_data = len(data['result'])
        if current_watched == 0:
            data = data['result']
        else:
            data = data['result'][:-current_watched]
        user.watched = size_of_current_data
        user.save()
        for x in data:
            if x['verdict'] == 'OK' and x['contestId'] < 10**5:
                problem = Problem.objects.get(problem_name=x['problem']['name'], contest_id = x['problem']['contestId'])
                solved = problem.solved
                tags = [x.name for x in problem.tag_set.all()]
                for _tag in tags:
                    update_user_tag_relationship(username, _tag, solved)

def find_in_cf(username):

    USERNAME = ""

    try:
        USERNAME = str(username)
    except:
        return False

    request_result = requests.get('http://codeforces.com/api/user.info?handles={}'.format(USERNAME))
    request_result = request_result.text
    result_data = json.loads(request_result)
    if result_data['status'] != 'OK':
        return None
    return int(result_data['result'][0]['rating'])


def login(request):


    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('handle', '')
        password = username
        error = ""
        rating = find_in_cf(username)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            update_user(username, rating)
            return redirect('/')
        else:
                if rating is not None:
                    tmp = request.POST
                    tmp['username'] = username
                    tmp['password2'] = username
                    tmp['password1'] = username

                    try:
                        del tmp['password']
                        del tmp['handle']
                    except:
                        pass

                    userform = UserCreationForm(tmp)
                    userform.save()
                    newuser = auth.authenticate(username=username, password=username)
                    auth.login(request,newuser)
                    update_user(username, rating)
                    return redirect('/')
                else:
                    error = error + "You are not registered at codeforces.com"
                args['login_error'] = error
                return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)