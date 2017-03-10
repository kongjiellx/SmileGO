#coding:utf-8
import os, random
import numpy as np

class controler(object):
    def __init__(self):
        self.index = 0

    # 处理一个sgf文件，返回落子序列
    def deal_sgf(self, path):
        fp = open(path, 'r')
        for line in fp:
            if line.startswith('AB') or line.startswith('AW'):
                raise Exception('not normal sgf file')
            if line.startswith(';'):
                tmoves = line.split(';')
                moves = []
                for m in tmoves:
                    if len(m) == 5 and (m.startswith('W') or m.startswith('B')) and m[2].isalpha() and m[3].isalpha():
                        moves.append(m)
                return moves
        raise Exception('not normal sgf file')

    def deal_move(self, move):
        if move.startswith('B'):
            black_or_white = 1
        else:
            black_or_white = 2
        coordinates = move[2:4]
        return (black_or_white, (ord(coordinates[0]) - ord('a'), ord(coordinates[1]) - ord('a')))

    def one_hot(self, num, depth):
        a = np.zeros((depth,))
        a[num] = 1
        return a

    def pre_x_y(self, path='kgs-19-2017-01-new/'):
        docs = os.listdir(path)
        games = []
        for doc in docs:
            try:
                games.append(self.deal_sgf(path + doc))
            except:
                pass
        x = []  # 当前棋盘状态
        x2 = [] # 1表示该黑棋走， 2表示该白棋走
        y = []  # label
        for game in games:
            # 记录棋盘状态，对每个位置，0表示无子，1表示黑子，2表示白子
            game_state = np.zeros(shape=(19, 19))
            for move in game:
                game_state_chanle = []
                for i in range(len(game_state)):
                    for j in range(len(game_state[i])):
                        game_state_chanle.append(self.one_hot(game_state[i][j], 3)) # chanel[0]:空 chanel[1]:黑 chanel2:白
                x.append(game_state_chanle)
                # next_move形如(1, (5, 6))表示下一步为黑棋走子，落子坐标为(5, 6)
                next_move = self.deal_move(move)
                x2.append(self.one_hot(next_move[0] - 1, 2))
                y.append(self.one_hot(next_move[1][0] * 19 + next_move[1][1], 361))
                game_state[next_move[1][0]][next_move[1][1]] = next_move[0]
        self.data = (np.array(x), np.array(x2), np.array(y))
        self.data_len = len(x)
        print('%d train data!', self.data_len)
        assert len(x) == len(x2) == len(y)
        return np.array(x), np.array(x2), np.array(y)

    def get_batch(self, batch_size):
        if self.index + batch_size <= self.data_len:
            ret = self.data[0][self.index: self.index + batch_size], self.data[1][self.index: self.index + batch_size], self.data[2][self.index: self.index + batch_size]
            self.index += batch_size
            return ret
        else:
            # random.shuffle(self.data)
            self.index = 0
            print('epoch down!')
            return self.get_batch(batch_size)
