# Ultimate-Tic-Tac-Toe-using-AlphaZero
Ultimate Tic Tac Toe using the AlphaZero algorithm

## About the project

[![UTTT screenshot][uttt_screenshot]]

This is my senior project made by me and my teammates as a computer science student in National Taipei University. In this project, our target is to research how classical games are mastered by the Alphazero program and to do so, we have chosen Ultimate Tic Tac Toe as a medium-to-hard level game to be our main subject. The whole project is written using Python.

Introduction to Alphazero:
AlphaZero is a computer program developed by artificial intelligence research company DeepMind to master the games of chess, shogi and go. Known for beating the world-champion program in each case, Alphazero learns everything from zero through pure self play. The concept of Alphazero is replacing hand-crafted rules with a deep neural network and general purpose algorithms that know nothing about the game beyond the basic rules.

Ultimate Tic Tac Toe rules:
Ultimate Tic Tac Toe is a much more strategic version of Tic Tac Toe. In Ultimate Tic Tac Toe, unlike the 9-square grid board in the normal Tic Tac Toe, we have a smaller 9-square grid inside the 9-square grid board, therefore a total of 81 squares in the whole board. The game starts with a player playing wherever they want in any of the 81 empty spots. This move "sends" their opponent to its relative location. For example, if X played in the top right square of their local board, then O needs to play next in the local board at the top right of the global board. O can then play in any one of the nine available spots in that local board, each move sending X to a different local board. If a move is played so that it is to win a local board by the rules of normal tic-tac-toe, then the entire local board is marked as a victory for the player in the global board. Once a local board is won by a player or it is filled completely, no more moves may be played in that board. If a player is sent to such a board, then that player may play in any other board. Pretty hard? Yes.

This project consists of 8 main programs:
- game.py: the game itself
- dual_network.py: structure of the neural network
- pv_mcts.py: predicting the next move using the neural network and implementing the Monte-Carlo tree search method, outputs the policy value of each legal move
- self_play.py: playing the game using pv_mcts againts itself
- train_network.py: training the neural network based on the data obtained through self play
- evaluate_network.py: evaluates the trained model
- evaluate_best_player.py: playing the game against different algorithms(random, alpha-beta, mcts)
- train_cycle.py: runs all the program above in a cycle

Added feature: dynamic simulation in pv_mcts. previously, pv_mcts simulates the legal moves for a fixed number of iteration, now it uses a simple algorithm to minimize the number of iteration. This is efficient for self play because each game now takes a faster time to finish.

NOTE: this project is still ongoing
