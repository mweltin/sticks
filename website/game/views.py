from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import csv

# importing sys
import sys
# adding Folder_2 to the system path
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from rules import rules
from environment import env


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
    state_index = env.state_table.index(data['state'])
    '''
        action_table = [
        [Actions.SWAP],
        [Actions.LEFT, Actions.LEFT],
        [Actions.LEFT, Actions.RIGHT],
        [Actions.RIGHT, Actions.RIGHT],
        [Actions.RIGHT, Actions.LEFT]
    ]
    '''
    if data['playerType'] == 'human':
        # def step(state_idx, player_idx, action_idx):
        new_state = env.step(state_index, 0, [1, 1])
    else:
        with open('qlearning/q_table.csv', mode='r')as file:
            q_table = csv.reader(file)

        new_state = env.step(state_index, 1, [1, 1])
    return JsonResponse(new_state, safe=False)
