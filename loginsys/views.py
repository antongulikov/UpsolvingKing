import requests
import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from users.models import UpUser, Problem
from helpscript.additon import *
from threading import Thread

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
            if x['verdict'] == 'OK' and x['contestId'] < 10**5 and len(x['problem']['tags']) > 0:
                problem = None
                if len(Problem.objects.filter(problem_name=x['problem']['name'], contest_id = x['problem']['contestId'], problem_id = x['problem']['index'])) > 0:
                    problem = Problem.objects.filter(problem_name=x['problem']['name'], contest_id = x['problem']['contestId'], problem_id = x['problem']['index'])[0]
                elif len(Problem.objects.filter(problem_name=x['problem']['name'], contest_id = (-1+x['problem']['contestId']), problem_id = x['problem']['index'])) > 0:
                    problem = Problem.objects.filter(problem_name=x['problem']['name'], contest_id = (-1 + x['problem']['contestId']), problem_id = x['problem']['index'])[0]
                else:
                    print 2
                    continue
                if problem is None:
                    continue
                problem.users.add(user)
                problem.save()
                solved = problem.solved
                for _tag in problem.tag_set.all():
                    update_user_tag_relationship(user, _tag, solved)


class UpdateThread(Thread):

    def __init__(self, username, rating):
        Thread.__init__(self)
        self.username = username
        self.rating = rating

    def run(self):
        if len(UpUser.objects.filter(username=self.username)) == 0:
            user = UpUser(username=self.username, rating=self.rating, isActive = False)
            user.save()
        if user.isActive:
            return
        user.isActive = True
        user.save()
        update_user(self.username, self.rating)
        user.isActive = False
        user.save()



def logout(request):
    auth.logout(request)
    return redirect('/')


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
    try:
        return int(result_data['result'][0]['rating'])
    except:
        return 0


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
            updUser = UpdateThread(username, rating)
            updUser.start()
            #update_user(username, rating)
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
                    updUser = UpdateThread(username, rating)
                    updUser.start()

                    #update_user(username, rating)
                    return redirect('/')
                else:
                    error = error + "You are not registered at codeforces.com"
                args['login_error'] = error
                return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)

def updateInf(request):
    username = ""
    try:
        username = auth.get_user(request).username
    except:
        return redirect('/')
    rating = find_in_cf(username)
    updUser = UpdateThread(username, rating)
    updUser.start()

    #update_user(username, rating)
    return redirect('/')
