import numpy as np
import random
import math

class State:
    def __init__(self, pieces=None, enemy_pieces=None, win_boards = None, lose_boards = None, draw_boards = None, board = None):
        self.pieces = pieces if pieces != None else [0] * 81
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0] * 81
        self.win_boards = win_boards if win_boards != None else [0] * 9
        self.lose_boards = lose_boards if lose_boards != None else [0] * 9
        self.draw_boards = draw_boards if draw_boards != None else [0] * 9
        self.board = board
    
    def piece_count(self, pieces):
        count = np.sum(pieces)
        return count
    
    def get_board_range(self, board):
        boardRange = []
        r1 = board * 9
        r2 = r1 + 9
        boardRange.append(r1)
        boardRange.append(r2)
        return boardRange
    
    def get_next_board(self, action):
        for i in range(9):
            r = self.get_board_range(i)
            count = 0
            for j in range(r[0], r[1]):
                if action == j:
                    return count
                count += 1
                
    def get_board_num(self, action):
        for i in range(9):
            r = self.get_board_range(i)
            if action >= r[0] and action < r[1]:
                return i
        
    def is_lose(self, flag):
        def is_comp(flag, x, y, dx, dy):  
            if flag == 0:
                r = self.get_board_range(self.board)
                row = self.enemy_pieces[r[0]:r[1]]
            else:
                row = self.lose_boards
                
            for _ in range(3):
              if y < 0 or 2 < y or x < 0 or 2 < x or \
                row[x+y*3] == 0:
                return False
              x, y = x+dx, y+dy
            return True

        if is_comp(flag, 0, 0, 1, 1) or is_comp(flag, 0, 2, 1, -1):
          return True
        for i in range(3):
          if is_comp(flag, 0, i, 1, 0) or is_comp(flag, i, 0, 0, 1):
            return True
        return False
    
    def is_draw(self, flag):
        if flag == 0:
            r = self.get_board_range(self.board)
            return self.piece_count(self.pieces[r[0]:r[1]]) + self.piece_count(self.enemy_pieces[r[0]:r[1]]) == 9
        else:
            return self.piece_count(self.win_boards) + self.piece_count(self.lose_boards) + self.piece_count(self.draw_boards) == 9
    
    def is_done(self):
        return self.is_lose(1) or self.is_draw(1)
    
    def update_state(self):
        board = self.board
        for i in range(9):
            self.board = i
            if self.is_lose(0):
                self.lose_boards[i] = 1
            if self.is_draw(0) and self.win_boards[i] == 0 and self.lose_boards[i] == 0:
                self.draw_boards[i] = 1
        self.board = board
    
    def next(self, action):
        pieces = self.pieces.copy()
        pieces[action] = 1
        return State(self.enemy_pieces, pieces, self.lose_boards, self.win_boards, self.draw_boards, self.get_board_num(action))

    def legal_boards(self):
        board = self.board
        boards = []
        if board == None or self.win_boards[board] == 1 or self.lose_boards[board] == 1 or self.draw_boards[board] == 1:
            for i in range(9):
                if self.win_boards[i] == 0 and self.lose_boards[i] == 0 and self.draw_boards[i] == 0:
                    boards.append(i)
        else:
            boards.append(board)       
        return boards
    
    def legal_actions(self):
        boards = self.legal_boards()
        actions = []
        for board in boards:
            r = self.get_board_range(board)
            for i in range(r[0], r[1]):
                if self.pieces[i] == 0 and self.enemy_pieces[i] == 0:
                    actions.append(i)       
        return actions
    
    def is_first_player(self):
        return self.piece_count(self.pieces) == self.piece_count(self.enemy_pieces)

    def __str__(self):
        ox = (' O ', ' X ') if self.is_first_player() else (' X ', ' O ')
        output = ''
        
        pieces = []
        enemy_pieces = []
        for i in range(9):
            r = self.get_board_range(i)
            pieces.append(self.pieces[r[0]:r[1]])
            enemy_pieces.append(self.enemy_pieces[r[0]:r[1]])
        
        temp1 = 0
        for _ in range(3):
            temp2 = 0
            for _ in range(3):
                for i in range(temp1,temp1+3):
                    for j in range(temp2, temp2+3):
                        if pieces[i][j] == 1:
                            output += ox[0]
                        elif enemy_pieces[i][j] == 1:
                            output += ox[1]
                        else:
                            output += ' - '
                temp2 += 3
                output += '\n'
            temp1 += 3
        return output
       
def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0, len(legal_actions)-1)]

def alpha_beta(state, alpha, beta):
  if state.is_lose(0):
    return -1
  if state.is_draw(0):
    return 0
  
  for action in state.legal_actions():
    score = -alpha_beta(state.next(action), -beta, -alpha)
    if score > alpha:
      alpha = score
    if alpha >= beta:
      return alpha
  
  return alpha

def alpha_beta_action(state):
  best_action = 0
  alpha = -float('inf')
  for action in state.legal_actions():
    score = -alpha_beta(state.next(action), -float('inf'), -alpha)
    if score > alpha:
      best_action = action
      alpha = score
  return best_action

def playout(state):
    if state.is_lose(0):
      return -1
    if state.is_draw(0):
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
              value = -1 if self.state.is_lose(1) else 0
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

if __name__ == '__main__':
    state = State()
    while True:
        state.update_state()
        if state.is_done():
            break
        action = mcts_action(state)
        state = state.next(action)
        state.board = state.get_next_board(action)
        print(state)