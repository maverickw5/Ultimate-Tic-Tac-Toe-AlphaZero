import random
import math

def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0, len(legal_actions)-1)]

def playout(state):
    if state.is_lose(None):
      return -1
    if state.is_draw(None):
      return 0

    return -playout(state.next(random_action(state)))

def argmax(collection, key=None):
    return collection.index(max(collection))

def mcts_action(state):
    class Node:
        def __init__(self, state):
            self.state = state
            self.w = 0
            self.n = 0
            self.child_nodes = None

        def evaluate(self):
            if self.state.is_done():
              value = -1 if self.state.is_lose(None) else 0
              self.w += value
              self.n += 1
              return value
            if not self.child_nodes:
              value = playout(self.state)
              self.w += value
              self.n += 1
              if self.n == 10:
                self.expand()
              return value
            else:
              value = -self.next_child_node().evaluate()
              self.w += value
              self.n += 1
              return value
        
        def expand(self):
            legal_actions = self.state.legal_actions()
            self.child_nodes = []
            for action in legal_actions:
              self.child_nodes.append(Node(self.state.next(action)))
      
        def next_child_node(self):
            for child_node in self.child_nodes:
              if child_node.n == 0:
                return child_node
            t = 0
            for c in self.child_nodes:
              t += c.n
            ucb1_values = []
            for child_node in self.child_nodes:
              ucb1_values.append(-child_node.w/child_node.n+(2*math.log(t)/child_node.n)**0.5)
            return self.child_nodes[argmax(ucb1_values)]

    root_node = Node(state)
    root_node.expand()
    for _ in range(100):
      root_node.evaluate()
    legal_actions = state.legal_actions()
    n_list = []
    for c in root_node.child_nodes:
      n_list.append(c.n)
    return legal_actions[argmax(n_list)]