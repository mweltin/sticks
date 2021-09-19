from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.

def index(request):
    template = loader.get_template('game/index.html')
    context = {
        'welcome': 'Welcome to the sticks game:',
    }
    return HttpResponse(template.render(context, request))