from django.shortcuts import render_to_response, render
from django.core.context_processors import csrf
from users.models import *

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
        pass
    else:
        return render_to_response('generatePage.html', args)