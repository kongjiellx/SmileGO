#coding:utf-8
import os
import numpy as np

# 处理一个sgf文件，返回落子序列
def deal_sgf(path):
    fp = open(path, 'r')
    for line in fp:
        if line.startswith('AB') or line.startswith('AW'):
            raise Exception('not normal sgf file')
        if line.startswith(';'):
            tmoves = line.split(';')
            moves = []
            for m in tmoves:
                if m != '':
                    moves.append(m)
            return moves
    raise Exception('not normal sgf file')

def prepare_data(path='kgs-19-2017-01-new/'):
    docs = os.listdir(path)
    games = []
    for doc in docs:
        try:
            games.append(deal_sgf(path + doc))
        except:
            pass
    return games

def pre_x_y(games):
    x = []
    y = []
    for game in games:
        # 记录棋盘状态，对每个位置，0表示无子，1表示黑子，2表示白子
        game_state = np.zeros(shape=(19, 19))
        for move in game:
