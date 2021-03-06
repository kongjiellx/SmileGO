#!/usr/bin/env python
# coding: utf-8

import pygame
import go
import numpy as np

from utils import *

BACKGROUND = 'images/small.jpg'
BOARD_SIZE = (630, 630)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.display.set_caption('Goban')
screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
background = pygame.image.load(BACKGROUND).convert()

class Stone(go.Stone):
    def __init__(self, board, point, color):
        """Create, initialize and draw a stone."""
        super(Stone, self).__init__(board, point, color)
        self.coords = (15 + (self.point[0] + 1) * 30, 15 + (self.point[1] + 1) * 30)


    def draw(self):
        """Draw the stone as a circle."""
        pygame.draw.circle(screen, self.color, self.coords, 15, 0)
        pygame.display.update()

    def remove(self):
        """Remove the stone from board."""
        blit_coords = (self.coords[0] - 15, self.coords[1] - 15)
        area_rect = pygame.Rect(blit_coords, (30, 30))
        screen.blit(background, blit_coords, area_rect)
        pygame.display.update()
        super(Stone, self).remove()

class Board(go.Board):
    def __init__(self):
        """Create, initialize and draw an empty board."""
        super(Board, self).__init__()
        self.outline = pygame.Rect(45, 45, 540, 540)
        self.draw()

    def draw(self):
        """Draw the board to the background and blit it to the screen.

        The board is drawn by first drawing the outline, then the 19x19
        grid and finally by adding hoshi to the board. All these
        operations are done with pygame's draw functions.

        This method should only be called once, when initializing the
        board.

        """
        pygame.draw.rect(background, BLACK, self.outline, 3)
        # Outline is inflated here for future use as a collidebox for the mouse
        self.outline.inflate_ip(20, 20)
        for i in range(18):
            for j in range(18):
                rect = pygame.Rect(45 + (30 * i), 45 + (30 * j), 30, 30)
                pygame.draw.rect(background, BLACK, rect, 1)
        for i in range(3):
            for j in range(3):
                coords = (135 + (180 * i), 135 + (180 * j))
                pygame.draw.circle(background, BLACK, coords, 5, 0)
        screen.blit(background, (0,0))
        pygame.display.update()

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

    def get_x_for_model(self):
        game_state = np.zeros((19, 19))
        for group in self.groups:
            for stone in group.stones:
                if stone.color == BLACK:
                    game_state[stone.point[0] - 1][stone.point[1] - 1] = 1
                elif stone.color == WHITE:
                    game_state[stone.point[0] - 1][stone.point[1] - 1] = 2

        game_state_chanle = []
        for i in range(len(game_state)):
            for j in range(len(game_state[i])):
                game_state_chanle.append(one_hot(game_state[i][j], 3))  # chanel[0]:空 chanel[1]:黑 chanel2:白
        if self.next == BLACK:
            x2 = one_hot(0, 2)
        elif self.next == WHITE:
            x2 = one_hot(1, 2)
        return np.array(game_state_chanle).reshape((-1, 19, 19, 3)), np.array(x2).reshape((-1, 2))


