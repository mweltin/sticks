from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

# Create your views here.

def index(request):
    template = loader.get_template('game/index.html')
    context = {
        'welcome': 'Welcome to the sticks game:',
    }
    return HttpResponse(template.render(context, request))

def turn(request):
    data = {
        'human': [1,1],
        'qlearning': [2,3],
        'takenBy': 'human'
    }
    return JsonResponse(data, safe=False)