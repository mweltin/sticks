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
    data = data['turnData']
    state = [data['human']['playerState'], data['qlearning']['playerState']]
    state_index = env.state_table.index(state)
    if(data['activePlayer'] == 'human'):
        active_player_index = 0

    if (data['activePlayer'] == 'qlearning'):
        active_player_index = 1

    action_index = env.action_table.index( getActionArray(data) )

    if data['activePlayer'] == 'human':
        # def step(state_idx, player_idx, action_idx):
        new_state = env.step(state_index, 0, action_index)
    else:
        with open('../../../qlearning/q_table.csv', mode='r') as file:
            q_table = csv.reader(file)

    retval = env.step(state_index, 1, action_index)
    returnVal = {
        'state' : env.state_table[retval[0]],
        'hasWinner': retval[2]
    }
    return JsonResponse(returnVal, safe=False)


def getActionArray( data ):
    retval = []
    if data['human']['activeHand'] == 'right':
        retval.insert(0, 1)
    else:
         retval.insert(0, 0)

    if data['qlearning']['activeHand'] == 'right':
        retval.insert(1, 1)
    else:
        retval.insert(1, 0)

    return retval
