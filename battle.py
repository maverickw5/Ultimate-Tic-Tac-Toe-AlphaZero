from game import State, random_action, mcts_action
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K

SIMULATION_COUNT = 100
GAME_COUNT = 10

def first_player_point(ended_state):
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

def evaluate_with(label, next_actions):
    total_point = 0
    for i in range(GAME_COUNT):
        if i % 2 == 0:
            total_point += play(next_actions)
        else:
            total_point += 1 - play(list(reversed(next_actions)))
        print('\rGame {}/{}'.format(i+1, GAME_COUNT), end='')
    print('')
    average_point = total_point / GAME_COUNT
    print(label, average_point)

def battle(SIM):
    model = load_model('./model/best1.h5')
    next_pv_mcts_action = pv_mcts_action(model, SIM)
    next_actions = (next_pv_mcts_action, random_action)
    evaluate_with('BestModel vs Random', next_actions)
    next_actions = (next_pv_mcts_action, mcts_action)
    evaluate_with('BestModel vs MCTS', next_actions)
    K.clear_session()
    del model

if __name__ == '__main__':
    battle(SIMULATION_COUNT)