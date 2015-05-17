from django.shortcuts import render_to_response, render, redirect
from django.core.context_processors import csrf
from users.models import *
from helpscript.additon import generate_problems, point,rating_by_power

def generate(request, username):
    args = {}
    args.update(csrf(request))
    args['user'] = username
    user = UpUser.objects.get(username = username)
    tags = Tag.objects.all()
    tags = [x.name for x in tags]
    tags.append('nothing')
    tags.reverse()
    args['tags'] = tags
    if request.POST:
        tag1 = request.POST.get('tag1', '')
        tag2 = request.POST.get('tag2', '')
        tag3 = request.POST.get('tag3', '')        
        result = generate_problems(username, tag1, tag2, tag3)        
        args['problems'] = result
        cnt = 0
        data = {}
        for pr in result:
            tmp = TagProblem.objects.filter(problem=pr)
            lst = []
            for x in tmp:                
                if len(UserTag.objects.filter(user=user, tag=x.tag)) == 0:
                    UserTag.objects.create(user=user, tag=x.tag)
                tl = UserTag.objects.get(user=user, tag=x.tag)
                rating = point(user.rating, rating_by_power(tl.power), x.cnt_solved)
                name = x.tag.name
                lst.append((name, rating, x.cnt_solved))
            data[pr.problem_name] = lst
        args['data'] = data
        args['tag1'] = tag1
        args['tag2'] = tag2
        args['tag3'] = tag3
        return render_to_response('generatePage.html', args)
    else:
        return render_to_response('generatePage.html', args)