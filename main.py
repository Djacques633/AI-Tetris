import pygame
import time
import random

pygame.init()
screen = pygame.display.set_mode((400, 500))

# Figures:
square = [
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]

S = [[0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]]

L = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]

T = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0]]

J = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]]

Z = [[0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]

line = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
# shapes = [line, line]
shapes = [square, Z, L, T, line, S, J]


class Tetris:
    index = 0
    board = []
    width = 0
    height = 0
    x = 100
    y = 60
    zoom = 20
    score = 0
    figure = None
    game_over = False

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)

    def reset(self):
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = 0
        self.score = -1
        self.figure = None

    def __init__(self):

        self.width = 10
        self.height = 20
        self.score = -1
        self.board = []
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.board.append(new_line)

    def next_shape(self):
        self.index = random.randint(0, len(shapes) - 1)
        if self.index == len(shapes):
            self.index = 0
        self.figure = shapes[self.index]
        for x in range(len(self.figure)):
            for y in range(len(self.figure[x])):
                if self.figure[x][y] == 1 and self.board[x][y] == 0:
                    self.board[x][y] = 2
                elif self.figure[x][y] == 1 and self.board[x][y] == 1:
                    self.game_over = True
                    return

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
                self.score += 10
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.board[i1][j] = self.board[i1 - 1][j]

    def freeze(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 2:
                    self.board[i][j] = 1
        self.check_lines()
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
        time.sleep(.15)
        self.go_down()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if next_move == 0:
            self.right()
        elif next_move == 1:
            self.left()

        screen.fill(self.WHITE)
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 2:
                    pygame.draw.rect(screen, self.GRAY, [
                        self.x + self.zoom * j+1, self.y + self.zoom * i+1, self.zoom-1, self.zoom-1], 1)
                elif self.board[i][j] == 1:
                    pygame.draw.rect(screen, self.BLACK,
                                     [self.x + self.zoom * j+1, self.y + self.zoom * i+1, self.zoom-1, self.zoom-1])
                else:
                    pygame.draw.rect(screen, self.WHITE,
                                     [self.x + self.zoom * j+1, self.y + self.zoom * i+1, self.zoom-1, self.zoom-1])
        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score:" + str(self.score), True, self.GRAY)
        screen.blit(text, [0, 0])
        pygame.display.flip()
