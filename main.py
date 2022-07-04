from dual_network import dual_network
from self_play import self_play
from train_network import train_network
from evaluate_model import evaluate_model
from battle import battle

TRAIN_ITER = 10
SIMULATION_COUNT = 200

dual_network()

for i in range(TRAIN_ITER):
    print('Train',i,'=====================================')
    self_play(SIMULATION_COUNT)
    train_network()
    update_best_player = evaluate_model(SIMULATION_COUNT)
    if update_best_player:
        battle(SIMULATION_COUNT)