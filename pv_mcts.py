from game import State
from dual_network import DN_INPUT_SHAPE

from math import sqrt
from tensorflow.keras.models import load_model
from pathlib import Path
import numpy as np

DEF_PV_EVALUATE_COUNT = 50
MAX_PV_EVALUATE_COUNT = 162
PV_SCORE_THRESHOLD = 0.8
    
def predict(model, state):
    a, b, c = DN_INPUT_SHAPE
    x = np.array([state.pieces, state.enemy_pieces])
    x = x.reshape(c, a, b).transpose(1, 2, 0).reshape(1, a, b, c)
    y = model.predict(x, batch_size=1)
    policies = y[0][0][list(state.legal_actions())]
    policies /= sum(policies) if sum(policies) else 1
    value = y[1][0][0]
    return policies, value

def nodes_to_scores(nodes):
    scores = []
    for c in nodes:
        scores.append(c.n)
    return scores

def pv_mcts_scores(model, state, temperature):
    class node:
        def __init__(self, state, p):
            self.state = state
            self.p = p
            self.w = 0
            self.n = 0
            self.child_nodes = None
        
        def evaluate(self):
            if self.state.is_done():
                value = -1 if self.state.is_lose(1) else 0
                self.w += value
                self.n += 1
                return value
            if not self.child_nodes:
                policies, value = predict(model, self.state)
                self.w += value
                self.n += 1
                self.child_nodes = []
                for action, policy in zip(self.state.legal_actions(), policies):
                    self.child_nodes.append(node(self.state.next(action), policy))
                return value
            else:
                value = -self.next_child_node().evaluate()
                self.w += value
                self.n += 1
                return value
        
        def next_child_node(self):
            C_PUCT = 1.0
            t = sum(nodes_to_scores(self.child_nodes))
            pucb_values = []
            for child_node in self.child_nodes:
                pucb_values.append((-child_node.w/child_node.n if child_node.n else 0.0) + C_PUCT*child_node.p*sqrt(t)/(1+child_node.n))
            return self.child_nodes[np.argmax(pucb_values)]
    
    root_node = node(state, 0)
    if temperature == 0:
        for i in range(DEF_PV_EVALUATE_COUNT):
            root_node.evaluate()
        scores = nodes_to_scores(root_node.child_nodes)
        action = np.argmax(scores)
        scores = np.zeros(len(scores))
        scores[action] = 1
        return scores
    else:
        checkpoint_index = 1
        for i in range(MAX_PV_EVALUATE_COUNT+1):
            root_node.evaluate()
            if i == get_checkpoint(checkpoint_index):
                scores = nodes_to_scores(root_node.child_nodes)
                scores = boltzman(scores, temperature)
                if max(scores) >= PV_SCORE_THRESHOLD:
                    return scores
                checkpoint_index += 1
        return scores
            
def get_checkpoint(index):
    return index*18

def boltzman(xs, temperature):
    xs = [x ** (1 / temperature) for x in xs]
    return [x / sum(xs) for x in xs]

def pv_mcts_action(model, temperature=0):
    def pv_mcts_action(state):
        scores = pv_mcts_scores(model, state, temperature)
        return np.random.choice(state.legal_actions(), p=scores)
    return pv_mcts_action

if __name__ == '__main__':
    path = sorted(Path('./model').glob('*.h5'))[-1]
    model = load_model(str(path))
    state = State()
    next_action = pv_mcts_action(model, 1.0)
    while True:
        state.update_state()
        if state.is_done():
            break
        action = next_action(state)
        state = state.next(action)
        state.board = state.get_next_board(action)
        print(state)