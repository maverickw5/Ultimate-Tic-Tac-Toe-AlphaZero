from game import State
from pv_mcts import pv_mcts_scores
from dual_network import DN_OUTPUT_SIZE
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

SIMULATION_COUNT = 100 
EPISODE_COUNT = 100 #number of self-play iterations

def first_player_value(ended_state): #get value of finished state
    if ended_state.is_lose(None):
        return -1 if ended_state.is_first_player() else 1
    return 0

def play(model, SIM):
    #A 'history' consists: player's and opponent chosen move, policies, value 
    history = []
    move = 0
    state = State()
    while True:
        if state.is_done():
            break
        scores = pv_mcts_scores(model, state, SIM)
        policies = [0] * DN_OUTPUT_SIZE
        for action, policy in zip(state.legal_actions(), scores):
            policies[action] = policy
        history.append([[state.pieces, state.enemy_pieces], policies, None])
        action = np.random.choice(state.legal_actions(), p=scores)
        state = state.next(action)
        move += 1
    value = first_player_value(state)
    for i in range(len(history)):
        history[i][2] = value
        value = -value
    return history, move

def write_data(history): #keep record of every 'history'
    now = datetime.now()
    os.makedirs('./data/', exist_ok=True)
    path = './data/{:04}{:02}{:02}{:02}{:02}{:02}.history'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    with open(path, mode='wb') as f:
        pickle.dump(history, f)

def self_play(SIM):
    history = []
    moves = []
    model = load_model('./model/best.h5')
    for i in range(EPISODE_COUNT):
        h, m = play(model, SIM)
        history.extend(h)
        moves.append(m)
        print('\rSelfPlay {}/{}'.format(i+1, EPISODE_COUNT), end='')
    print('')
    write_data(history)
    K.clear_session()
    del model
    plt.plot(moves)
    plt.title('moves')
    plt.ylabel('number of moves')
    plt.xlabel('episode')
    plt.show()

if __name__ == '__main__':
    self_play(SIMULATION_COUNT)