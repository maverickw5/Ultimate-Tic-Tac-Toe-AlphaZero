from game import State, random_action, mcts_action
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
import tkinter as tk
import timeit

model = load_model('./model/best.h5')

class UI(tk.Frame):
    def __init__(self, master=None, model=None):
        print('Number of simulations per move:', end=' ')
        SIM = input()
        tk.Frame.__init__(self, master)
        self.master.title('Ultimate Tic Tac Toe Demo')
        self.state = State()
        self.next_action = pv_mcts_action(model, int(SIM))
        self.move = 0
        self.flag = True
        self.c = tk.Canvas(self, width=720, height=750, highlightthickness=0)
        self.c.bind('<Button-1>', self.turn_of_human) #Human vs AI, change to turn_of_random for Random vs AI
        self.c.pack()
        self.on_draw()

    def turn_of_human(self, event):
        if event.y > 720:
            self.state = State()
            self.move = 0
            self.flag = True
            self.on_draw()
        else:
            self.check_state()
            if self.flag:
                if not self.state.is_first_player():
                    return
                x = int(event.x/80)
                y = int(event.y/80)
                if x < 0 or 8 < x or y < 0 or 8 < y:
                    return
                if y<3:
                    action = (x%3) + int(x/3)*9 + 3*y
                if y>=3 and y<6:
                    action = (x%3) + int(x/3)*9 + 3*y+18
                if y>=6:
                    action = (x%3) + int(x/3)*9 + 3*y+36

                if not action in self.state.legal_actions():
                    return
                else:
                    self.move += 1
                    print("(Player) Move", self.move)
                self.state = self.state.next(action)
                str_action = str(int(action/9)+1)+','+str(action%9+1)
                print('Action:', str_action)
                print()
                self.check_state()
                self.master.after(1, self.turn_of_ai)

    def turn_of_ai(self):
        self.check_state()
        if self.flag:
            self.move += 1
            print("(AI) Move", self.move)
            print('Legal action(s):', self.state.legal_actions())
            start = timeit.default_timer()
            scores, action = self.next_action(self.state)
            stop = timeit.default_timer()
            print('Score(s):', scores)
            self.state = self.state.next(action)
            str_action = str(int(action/9)+1)+','+str(action%9+1)
            print('Action:', str_action)
            print('Execution time:', stop - start, end=' sec\n\n')
            self.check_state()

    def turn_of_random(self, event):
        if event.y > 720:
            self.state = State()
            self.move = 0
            self.flag = True
            self.on_draw()
        else:
            self.check_state()
            if self.flag:
                self.move += 1
                print("(Random) Move", self.move)
                action = random_action(self.state)
                self.state = self.state.next(action)
                str_action = str(int(action/9)+1)+','+str(action%9+1)
                print('Action:', str_action)
                print()
                self.check_state()
                self.master.after(1, self.turn_of_ai)

    def check_state(self):
        if not self.flag:
            print('Restart')
        elif self.state.is_done():
            self.on_draw()
            if self.state.is_lose(None):
                print('Lost') if self.state.is_first_player() else print('Win')
            else:
                print('Draw')
            self.flag = False
            return
        else:
            self.on_draw()

    def draw_piece(self, index, first_player):
        x = index%9*80+10
        y = int(index/9)*80+10
        if first_player:
            self.c.create_oval(x, y, x+60, y+60, width=2.0, outline='#FFFFFF')
        else:
            self.c.create_line(x, y, x+60, y+60, width=2.0, fill='#5D5D5D')
            self.c.create_line(x+60, y, x, y+60, width=2.0, fill='#5D5D5D')
    
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 720, 720, width=0.0, fill='#00A0FF')
        self.c.create_rectangle(0, 720, 720, 750, width=0.0, fill='#FF0000')
        for i in range(8):
            if i == 2 or i == 5:
                self.c.create_line(80*(i+1), 0, 80*(i+1), 720, width=2.0, fill='#FF0000')
                self.c.create_line(0, 80*(i+1), 720, 80*(i+1), width=2.0, fill='#FF0000')
            else:
                self.c.create_line(80*(i+1), 0,80*(i+1), 720, width=2.0, fill='#0077BB')
                self.c.create_line(0, 80*(i+1), 720, 80*(i+1), width=2.0,fill='#0077BB')
        for i in range(9):
            x=i%3*240+10
            y=int(i/3)*240+10
            if self.state.is_first_player():
                if self.state.boards[i]==1 and self.state.enemy_boards[i]==0:
                    self.c.create_line(x+10, y+10, x+210, y+210, width=10.0, fill='#5D5D5D')
                    self.c.create_line(x+210, y+10, x+10, y+210, width=10.0, fill='#5D5D5D')
                elif self.state.enemy_boards[i]==1 and self.state.boards[i]==0:
                    self.c.create_oval(x+10, y+10, x+210, y+210, width=10.0, outline='#FFFFFF')
            else:
                if self.state.enemy_boards[i]==1 and self.state.boards[i]==0:
                    self.c.create_line(x+10, y+10, x+210, y+210, width=10.0, fill='#5D5D5D')
                    self.c.create_line(x+210, y+10, x+10, y+210, width=10.0, fill='#5D5D5D')
                elif self.state.boards[i]==1 and self.state.enemy_boards[i]==0:
                    self.c.create_oval(x+10, y+10, x+210, y+210, width=10.0, outline='#FFFFFF')
        for i in range(81):
            draw=[0,1,2,9,10,11,18,19,20,3,4,5,12,13,14,21,22,23,6,7,8,15,16,17,24,25,26,27,28,29,36,37,38,45,46,47,30,31,32,39,40,41,48,49,50,33,34,35,42,43,44,51,52,53,54,55,56,63,64,65,72,73,74,57,58,59,66,67,68,75,76,77,60,61,62,69,70,71,78,79,80]
            if self.state.pieces[i] == 1:
                i=draw[i]
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                i=draw[i]
                self.draw_piece(i, not self.state.is_first_player())

f = UI(model=model)
f.pack()
f.mainloop()