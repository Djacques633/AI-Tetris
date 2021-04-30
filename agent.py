import torch
import random
import numpy as np
from main import Tetris
from collections import deque
import copy


class Agent:
    figure = None
    games = 0
    # Pick which play method the AI will follow
    play_method = ['RANDOM', 'MATCH', 'HOLE']
    choice = 3
    front_pass = True
    board = []
    height = 20
    width = 10

    def __init__(self):
        pass

    def get_piece_width(self, piece):
        width = 0
        for i in range(len(piece[0])):
            for j in range(len(piece)):
                if piece[j][i] == 1:
                    width += 1
                    continue
        return width

    def will_complete_line(self, board, piece, game):
        for i in range(game.width - self.get_piece_width(piece)):
            for j in range(game.height):
                if game[j][i] == 0 and game[j + 1][i] == 1:
                    pass
                if game[j][i] == 0 or game[j][i] == 2:
                    pass

        return -1

    def find_highest_point(self, game):
        for x in range(game.height):
            for y in range(game.width):
                if self.board[x][y] == 1:
                    return x
        return 0

    def predict_best_move(self, board, piece, game):

        if self.play_method[self.choice] == 'RANDOM':
            move = random.randint(0, 2)
            return move

        elif self.play_method[self.choice] == 'HOLE':
            self.figure = copy.copy(game.figure)
            count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(game.width):
                # Simulate
                holes = 0
                self.figure = copy.deepcopy(game.figure)
                self.board = copy.deepcopy(game.board)
                while self.figure != None:
                    move = self.min_to_left(i, self.board, game)
                    self.game_loop(move)
                # Evaluate
                highest_point = self.find_highest_point(game)
                for x in range(highest_point, game.height):
                    for y in range(game.width):
                        if self.board[x][y] == 0:
                            if self.board[x-1][y] and self.board[x-1][y] == 1:
                                holes += 3
                                self.board[x][y] = 1
                            elif x + 1 < game.height and self.board[x + 1][y] == 1:
                                holes += 1
                            elif y + 1 < game.width and self.board[x][y + 1] == 1:
                                holes += 1
                            elif y-1 > 0 and self.board[x][y-1] == 1:
                                holes += 1
                if self.check_lines():
                    count[i] = -1
                else:
                    count[i] = holes
                holes = 0
            best_move = count.index(min(count))
            return self.min_to_left(best_move, board, game)

        elif self.play_method[self.choice] == 'MATCH':
            count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            for i in range(game.width):
                for j in range(game.height):
                    if board[j][i] == 1:
                        count[i] += 1
                    pass

            min_index = count.index(min(count))
            return self.min_to_left(min_index, board, game)

    def min_to_left(self, min_index, board, game):
        choice = 2
        for i in range(game.width):
            for j in range(game.height):
                if board[j][i] == 2 and min_index == i:
                    return 2
                if board[j][i] == 2 and min_index < i:
                    choice = 1
                    return 1
                elif board[j][i] == 2 and min_index > i:
                    choice = 0
                    return 0
        return choice

    def go_down(self):
        for i in range(self.height):
            for j in range(self.width):
                if i == 19 and self.board[i][j] == 2:
                    self.freeze()
                    return
                if (self.board[i][j] == 2 and (self.board[i + 1][j] == 2 or self.board[i + 1][j] == 0)) or self.board[i][j] == 0 or self.board[i][j] == 1:
                    continue
                else:
                    self.freeze()
                    return
        for i in range(self.height - 1, -1, -1):
            for j in range(self.width - 1, -1, -1):
                if self.board[i][j] == 2:
                    self.board[i + 1][j] = 2
                    self.board[i][j] = 0

    def check_lines(self):
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.board[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                return True
            return False

    def freeze(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 2:
                    self.board[i][j] = 1
        self.figure = None

    def print_board(self):
        for i in range(self.height):
            print(self.board[i])

    def right(self):
        for i in range(self.width - 1, -1, -1):
            for j in range(self.height - 1, -1, -1):
                if (self.board[j][i] == 2 and i == self.width - 1) or (self.board[j][i] == 2 and self.board[j][i+1] == 1):
                    return
                elif self.board[j][i] == 2:
                    self.board[j][i] = 0
                    self.board[j][i + 1] = 2

    def left(self):
        for i in range(self.width):
            for j in range(self.height):
                if (self.board[j][i] == 2 and i == 0) or (self.board[j][i] == 2 and self.board[j][i-1] == 1):
                    return
                elif self.board[j][i] == 2:
                    self.board[j][i] = 0
                    self.board[j][i - 1] = 2

    def game_loop(self, next_move):
        if self.figure == None:
            self.next_shape()
            self.score += 1
        self.go_down()
        if next_move == 0:
            self.right()
        elif next_move == 1:
            self.left()


def train():
    record = 0
    game = Tetris()
    agent = Agent()
    while True:
        board = game.board
        agent.board = game.board
        piece = game.figure
        next_move = agent.predict_best_move(board, piece, game)
        game.game_loop(next_move)
        if game.game_over:
            print("Game", agent.games, "over")
            agent.games += 1
            if game.score > record:
                record = game.score
                print("New high score:", record)

            game.reset()
            game.game_over = False


train()
