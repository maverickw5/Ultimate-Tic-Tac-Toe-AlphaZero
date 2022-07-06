# Ultimate-Tic-Tac-Toe-using-AlphaZero
### Ultimate Tic Tac Toe using the AlphaZero algorithm

## About the project

![UTTT screenshot][uttt_screenshot]

This is my senior project made by me and my teammates as computer science students in National Taipei University. In this project, our target is to research how classical games are mastered by the Alphazero program and to do so, we have chosen Ultimate Tic Tac Toe as a medium-to-hard level game to be our main subject.

Introduction to Alphazero: AlphaZero is a computer program developed by artificial intelligence research company DeepMind to master the games of chess, shogi and go. Known for beating the world-champion program in each case, Alphazero learns everything from zero through pure self play. The concept of Alphazero is replacing hand-crafted rules with a deep neural network and general purpose algorithms that know nothing about the game beyond the basic rules.

Ultimate Tic Tac Toe Rules: https://www.thegamegal.com/2018/09/01/ultimate-tic-tac-toe/

Note: If smaller grids that result in a tie, here we count it as neither X nor O

## Getting Started
### Prerequisites
Make sure you have the following installed on your computer:
* Python
* Tensorflow
* tkinter

### Installation
Clone the repo
 ```sh
 git clone https://github.com/github_username/repo_name.git
 ```
 
## Training
Follow these steps:
1. Configure the training variables. There are 3 variables that can be configured
   - Number of self play episodes (in self_play.py)
   - Number of network training epoch (in train_network.py)
   - Number of games for evaluation and best model update threshold (in evaluate_model.py)
   - Number of simulations per move (in main.py)
2. Open UTTT_train.ipynb in Jupyter Notebook
3. Start training

Notes:
- In each training cycle, a history file created by self play will be saved a folder named 'data'
- The best model will be used in the training cycles until a newly trained model beats the best model by a certain threshold

## Play against the model
Open command prompt and make sure the directory is in this repo's folder

Run demo.py
 ```sh
 python demo.py
 ```
 
![Demo screenshot][demo_screenshot]

[uttt_screenshot]: images/uttt_screenshot.png
[demo_screenshot]: images/demo_screenshot.png
