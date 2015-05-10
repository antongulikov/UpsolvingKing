from django.shortcuts import render_to_response, render, redirect
from django.core.context_processors import csrf
from users.models import *
from helpscript.additon import generate_problems

def generate(request, username):
    args = {}
    args.update(csrf(request))
    args['user'] = username
    tags = Tag.objects.all()
    tags = [x.name for x in tags]
    tags.append('nothing')
    tags.reverse()
    args['tags'] = tags
    if request.POST:
        tag1 = request.POST.get('tag1', '')
        tag2 = request.POST.get('tag2', '')
        tag3 = request.POST.get('tag3', '')
        print tag1, tag2, tag3
        result = generate_problems(username, tag1, tag2, tag3)
        args['problems'] = result
        return render_to_response('generatePage.html', args)
    else:
        return render_to_response('generatePage.html', args)