from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from shutil import copy

SIMULATION_COUNT = 100
GAME_COUNT = 20 #number of games to evaluate
UPDATE_THRESHOLD = 0.55 #score threshold

def first_player_point(ended_state): #gets value of finished state
    if ended_state.is_lose(None):
        return 0 if ended_state.is_first_player() else 1
    return 0.5  

def play(next_actions):
    state = State()
    while True:
        if state.is_done():
            break
        next_action = next_actions[0] if state.is_first_player() else next_actions[1]
        action = next_action(state)
        state = state.next(action)
    return first_player_point(state)  

def update_best_player(): #update best model to latest model
    copy('./model/latest.h5', './model/best.h5')
    print('BestModel Updated')

def evaluate_model(SIM):
    model0 = load_model('./model/latest.h5')
    model1 = load_model('./model/best.h5')
    next_action0 = pv_mcts_action(model0, SIM)
    next_action1 = pv_mcts_action(model1, SIM)
    next_actions = (next_action0, next_action1)
    total_point = 0
    for i in range(GAME_COUNT):
        if i % 2 == 0:
            total_point += play(next_actions)
        else:
            total_point += 1 - play(list(reversed(next_actions)))
        print('\rEvaluate {}/{}'.format(i+1, GAME_COUNT), end='')
    print('')
    average_point = total_point / GAME_COUNT
    print('Average Point:', average_point)
    K.clear_session()
    del model0
    del model1
    if average_point >= UPDATE_THRESHOLD:
        #update best model if average point is bigger or equal to the score threshold
        update_best_player()
        return True
    else:
        return False        

if __name__ == '__main__':
    evaluate_model(SIMULATION_COUNT)