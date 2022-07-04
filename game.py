import numpy as np
from mcts import random_action, mcts_action

class State:
    def __init__(self, pieces=None, enemy_pieces=None, boards = None, enemy_boards = None, action = None):
        #Initialize 5 variables
        #pieces: player's chosen moves, array size of 81
        #enemy_pieces: opponenent's chosen moves, array size of 81
        #boards: player's won boards, array size of 9
        #enemy_boards: opponent's won boards, array size of 9
        #boardNum: current board to play in (0 to 8)
        self.pieces = pieces if pieces != None else [0] * 81
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0] * 81
        if boards == None and enemy_boards == None:
            self.boards = [0] * 9
            self.enemy_boards = [0] * 9
        else:
            self.boards, self.enemy_boards = self.update_boards(boards.copy(), enemy_boards.copy(), action)
        self.boardNum = self.get_boardNum(action) if action != None else None
    
    def piece_count(self, pieces):
        count = np.sum(pieces)
        return count
    
    def get_board_range(self, boardNum): #get current board's range inside the 81 pieces
        boardRange = []
        r1 = boardNum * 9
        r2 = r1 + 9
        boardRange.append(r1)
        boardRange.append(r2)
        return boardRange
    
    def get_boardNum(self, action): #get next board to play based on move chosen
        return action%9
        
    def is_lose(self, boardNum): #check if player is lost
        def is_comp(boardNum, x, y, dx, dy):  
            if boardNum == None: #check for the whole board
                row = self.enemy_boards
            else: #check for the current board
                r = self.get_board_range(boardNum)
                row = self.enemy_pieces[r[0]:r[1]]
            for _ in range(3):
              if y < 0 or 2 < y or x < 0 or 2 < x or \
                row[x+y*3] == 0:
                return False
              x, y = x+dx, y+dy
            return True

        if is_comp(boardNum, 0, 0, 1, 1) or is_comp(boardNum, 0, 2, 1, -1):
          return True
        for i in range(3):
          if is_comp(boardNum, 0, i, 1, 0) or is_comp(boardNum, i, 0, 0, 1):
            return True
        return False
    
    def is_draw(self, boardNum): #check if state is draw
        if boardNum == None: #check for the whole board
            done_boards = [0]*9
            for i in range(9):
                if self.boards[i] == 1 or self.enemy_boards[i] == 1 or self.is_draw(i):
                    done_boards[i] = 1
            return self.piece_count(done_boards) == 9
        else: #check for the current board
            r = self.get_board_range(boardNum)
            return self.piece_count(self.pieces[r[0]:r[1]]) + self.piece_count(self.enemy_pieces[r[0]:r[1]]) == 9
    
    def is_done(self): #check if state is finish
        return self.is_lose(None) or self.is_draw(None)
    
    def update_boards(self, boards, enemy_boards, action):
        #marks the opponent's won board by 1 if current board is won by opponent
        boardNum = int(action/9)
        if self.is_lose(boardNum):
            enemy_boards[boardNum] = 1
        return enemy_boards, boards
    
    def next(self, action):
        #marks chosen move by 1 in the chosen move array
        #switch player's and opponent's chosen move array
        pieces = self.pieces.copy()
        pieces[action] = 1
        return State(self.enemy_pieces, pieces, self.boards, self.enemy_boards, action)

    def legal_board(self): #gets the legal board(s) to play in
        legal_board = []
        #get list of legal boards if the current board is already won, lost or draw, else returns the current board
        if self.boardNum == None or self.boards[self.boardNum] == 1 or self.enemy_boards[self.boardNum] == 1 or self.is_draw(self.boardNum):
            for i in range(9):
                if self.boards[i] == 0 and self.enemy_boards[i] == 0 and not self.is_draw(i):
                    legal_board.append(i)
        else:
            legal_board.append(self.boardNum)       
        return legal_board
    
    def legal_actions(self): #gets legal move(s) in legal board(s)
        legal_board = self.legal_board()
        actions = []
        for board in legal_board:
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

if __name__ == '__main__': #one game simulation
    state = State()
    next_actions = (random_action, mcts_action) #Random vs. MCTS
    while(True):
        if state.is_done():
            break
        next_action = next_actions[0] if state.is_first_player() else next_actions[1]
        action = next_action(state)
        state = state.next(action)
        print(state)