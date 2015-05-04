import requests
import json
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from users.models import UpUser
from problems.models import Problem


def logout(request):
    auth.logout(request)
    return redirect('/')

def create_users(username, password):
    try:
        user = 1 / len(UpUser.objects.filter(username=username))
    except:
        newUser = UpUser(username=username, password=password)
        newUser.save()
        q = requests.get('http://www.codeforces.com/api/user.status?handle={}&from=1&count=10000'.format(username))
        q = q.text
        data = json.loads(q)
        for x in data['result']:
            if x['verdict'] == 'OK':
                try:
                    new_problem = Problem(problem_name= x['problem']['name'],contest_id= x['problem']['contestId'], problem_id= x['problem']['index'])
                    new_problem.save()
                    new_problem.kings.add(newUser)
                except:
                    pass



def login(request):

    def find_in_codeforces(username, password):

        csrf_token = "5556167d8d70662bc4332055fe4000f5"
        try:
            USERNAME = str(username)
            PASSWORD = str(password)
        except:
            return False

        parts = {
            "csrf_token": csrf_token,
            "action": "enter",
            "handle":USERNAME,
            "password":PASSWORD,
            "_tta":"111",
            "ftaa":"41mqknjyviqj",
            "bfaa":"b12df922eb8f1e"
        }

        submit_addr = "http://codeforces.com/enter/"

        q = requests.get(submit_addr)
        r = q.content
        pos = r.find("-Token\" content=")
        r = r[pos+17:]
        csrf_token = r[:r.find('\"')]
        q = requests.post(submit_addr, data=parts, params={"csrf_token": csrf_token})
        return q.content.find("<div class=\"for-avatar\"><div class=\"avatar\"><a href=\"/profile/%s\">" % USERNAME) > -1




    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            create_users(username, password)
            return redirect('/')
        else:
            if find_in_codeforces(username, password):
                tmp = request.POST
                tmp['password2'] = password
                tmp['password1'] = password

                try:
                    del tmp['password']
                except:
                    pass

                userform = UserCreationForm(tmp)
                userform.save()
                newuser = auth.authenticate(username=username, password=password)
                auth.login(request,newuser)
                create_users(username, password)
                return redirect('/')
            else:
                args['login_error'] = "You are not registered at codeforces.com"
                return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)

