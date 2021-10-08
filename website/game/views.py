from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
import csv
import numpy as np

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
    active_player_index = None
    action_index = None
    data = json.loads(request.body)
    data = data['turnData']
    state = [data['qlearning']['playerState'], data['human']['playerState']]  # order is important
    state_index = env.state_table.index(state)
    if (data['activePlayer'] == 'human'):
        active_player_index = 1
        action_index = env.action_table.index(getActionArray(data))

    if (data['activePlayer'] == 'qlearning'):
        active_player_index = 0

    if data['activePlayer'] == 'qlearning':
        file_path = os.path.join(settings.FILES_DIR, 'q_table.csv')
        with open(file_path, mode='r') as file:
            q_table = list(csv.reader(file, quoting=csv.QUOTE_NONNUMERIC))

        action_index = np.nanargmax(q_table[state_index])

    retval = env.step(state_index, active_player_index, action_index)
    returnVal = {
        'state': env.state_table[retval[0]],
        'hasWinner': retval[2]
    }
    return JsonResponse(returnVal, safe=False)


@csrf_exempt
def swap(request):
    data = json.loads(request.body)
    data = data['turnData']
    if (data['activePlayer'] == 'human'):
        state = data['human']['playerState']
    if (data['activePlayer'] == 'qlearning'):
        state = data['qlearning']['playerState']
    state = rules.swap(state)
    return JsonResponse(state, safe=False)


"""
This is only called by the human player hence the human hand action is always at index zero.
"""


def getActionArray(data):
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
