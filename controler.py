#coding:utf-8
import os, random
import numpy as np
from utils import *
import go
import copy
import random

class AGame(go.Board):
    def __init__(self):
        """Create, initialize and draw an empty board."""
        super(AGame, self).__init__()

    def update_liberties(self, added_stone):
        """Updates the liberties of the entire board, group by group.

        Usually a stone is added each turn. To allow killing by 'suicide',
        all the 'old' groups should be updated before the newly added one.

        """
        for group in self.groups:
            if added_stone:
                if group == added_stone.group:
                    continue
            group.update_liberties()
        if added_stone:
            added_stone.group.update_liberties()

    def is_legal(self, added_stone):
        """Updates the liberties of the entire board, group by group.

        Usually a stone is added each turn. To allow killing by 'suicide',
        all the 'old' groups should be updated before the newly added one.

        """
        for group in self.groups:
            if added_stone:
                if group == added_stone.group:
                    continue
            group.update_liberties()
        return added_stone.group.is_legal()

# 处理一个sgf文件，返回落子序列
def deal_sgf(path):
    fp = open(path, 'r')
    moves = []
    for line in fp:
        if line.startswith('AB') or line.startswith('AW'):
            break
        if line.startswith(';'):
            tmoves = line.split(';')
            for m in tmoves:
                if len(m) == 5 and (m.startswith('W') or m.startswith('B')) and m[2].isalpha() and m[3].isalpha():
                    moves.append(m)
            break
    fp.close()
    return moves

def deal_move(move):
    if move.startswith('B'):
        black_or_white = go.BLACK
    else:
        black_or_white = go.WHITE
    coordinates = move[2:4]
    return (black_or_white, (ord(coordinates[0]) - ord('a'), ord(coordinates[1]) - ord('a')))

def get_panmian(board):
    ret = np.zeros((19, 19, 3))
    for group in board.groups:
        for stone in group.stones:
            if stone.color == go.WHITE:
                ret[stone.point[0]][stone.point[1]][2] = 1
            elif stone.color == go.BLACK:
                ret[stone.point[0]][stone.point[1]][1] = 1
    return ret

def get_liberities(board):
    ret = np.zeros((19, 19, 4))
    for group in board.groups:
        for stone in group.stones:
            assert len(stone.group.liberties) >= 1
            if len(stone.group.liberties) >= 4:
                ret[stone.point[0]][stone.point[1]][3] = 1
            else:
                ret[stone.point[0]][stone.point[1]][len(stone.group.liberties) - 1] = 1
    return ret

def get_liberties_after_move(board):
    ret = np.zeros((19, 19, 6))
    for i in range(19):
        for j in range(19):
            stone = board.search((i, j))
            if stone:
                continue

            fake_board = copy.deepcopy(board)
            fake_added_stone = go.Stone(fake_board, (i, j ), fake_board.turn((i, j)))
            if not fake_board.is_legal(fake_added_stone):
                continue

            fake_board.update_liberties(fake_added_stone)
            assert len(fake_added_stone.group.liberties) >= 1
            if len(fake_added_stone.group.liberties) >= 6:
                ret[i][j][5] = 1
            else:
                ret[i][j][len(fake_added_stone.group.liberties) - 1] = 1
    return ret

def get_legality(board):
    ret = np.zeros((19, 19, 1))
    for i in range(19):
        for j in range(19):
            stone = board.search((i, j))
            if stone:
                continue
            fake_board = copy.deepcopy(board)
            fake_added_stone = go.Stone(fake_board, (i, j), fake_board.turn((i, j)))
            if not fake_board.is_legal(fake_added_stone):
                ret[i][j][0] = 0
            else:
                ret[i][j][0] = 1
    return ret

def get_history(board):
    ret = np.zeros((19, 19, 3))
    for i in range(1, 4):
        if len(board.step_history) >= i:
            ret[board.step_history[-i][0]][board.step_history[-i][1]][i - 1] = 1
    return ret

def get_capture_size(board):
    pass

def get_black_white(board):
    if board.next == go.BLACK:
        return np.concatenate((np.ones((19, 19, 1)), np.zeros((19, 19, 1))), axis=2)
    else:
        return np.concatenate((np.zeros((19, 19, 1)), np.ones((19, 19, 1))), axis=2)

def deal_a_step(board):
    panmian = get_panmian(board)    # 盘面(19, 19 ,3)
    liberties = get_liberities(board)   # 气(19, 19, 4)
    # liberties_after_move = get_liberties_after_move(board)  # (19, 19 ,6)
    # legality = get_legality(board) # 合法性(19, 19, 1)
    history = get_history(board) #3步历史步数 (19, 19, 3)
    # capture_size = get_capture_size(board) #走当前位置可以提几子 (19, 19, 7)
    black_white = get_black_white(board) # 黑白(19, 19, 2)
    # return size (19, 19, 19)
    return np.concatenate((panmian, liberties, history, black_white), axis=2)

def pre_x_y(path='kgs-19-2017-01-new/'):
    docs = os.listdir(path)
    games = []
    num = 0
    random.shuffle(docs)
    for doc in docs:
        if num > 5:
            break
        num += 1
        one_game = deal_sgf(path + doc)
        if one_game != []:
            games.append(one_game)
    x = []  # x
    y = []  # label
    index = 0
    for game in games:
        if index % 10 == 0:
            print index
        index += 1
        agame = AGame()
        break_flag = False
        _x = []
        _y = []
        for move in game:
            # next_move形如(1, (5, 6))表示下一步为黑棋走子，落子坐标为(5, 6)
            next_move = deal_move(move)
            _x.append(deal_a_step(agame))
            _y.append(one_hot((next_move[1][0]) * 19 + next_move[1][1], 361))
            if next_move[0] != agame.next: # 有人pass
                break_flag = True
                break
            stone = agame.search(next_move[1])
            if stone:
                break_flag = True
                break
            try:
                added_stone = go.Stone(agame, next_move[1], agame.turn(next_move[1]))
                agame.update_liberties(added_stone)
            except:
                print 'error file!'
                break_flag = True
                break
        if not break_flag:
            x += _x
            y += _y

    return np.array(x, dtype='int8').reshape((-1, 19, 19, 12)), \
           np.array(y, dtype='int8')