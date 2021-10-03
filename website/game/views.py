from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# importing sys
import sys
# adding Folder_2 to the system path
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from rules import rules


# Create your views here.

def index(request):
    template = loader.get_template('game/index.html')
    context = {
        'welcome': 'Welcome to the sticks game:',
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def turn(request):
    data = json.loads(request.body)
    # state, active_player_index, action
    new_state = rules.take_turn([[1, 1], [1, 1]], 0, [1, 1])
    return JsonResponse(new_state, safe=False)
