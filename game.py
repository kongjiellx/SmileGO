from goban import *
import predict
import copy
from configure import *
from controler import deal_a_step

if __name__ == '__main__':
    board = Board()
    model = predict.load_model()
    print 'game start!'
    if mode == 'PVP':
        HUMAN_OR_AI = 'HUMAN'
        CHANGE = False
    elif mode == 'PVE':
        if HUMAN_COLOR == 'BLACK':
            HUMAN_OR_AI = 'HUMAN'
            CHANGE = True
        elif HUMAN_COLOR == 'WHITE':
            HUMAN_OR_AI = 'AI'
            CHANGE = True
    elif mode == 'EVE':
        HUMAN_OR_AI = 'AI'
        CHANGE = False
    while True:
        pygame.time.wait(5)
        if HUMAN_OR_AI == 'HUMAN':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and board.outline.collidepoint(event.pos):
                        x = int(round(((event.pos[0] - 5) / 40.0), 0))
                        y = int(round(((event.pos[1] - 5) / 40.0), 0))
                        stone = board.search(point=(x, y))
                        if stone:
                            pass
                        else:
                            fake_board = copy.deepcopy(board)
                            fake_added_stone = Stone(fake_board, (x, y), fake_board.turn((x, y)))
                            if not fake_board.is_legal(fake_added_stone):
                                pass
                            else:
                                added_stone = Stone(board, (x, y), board.turn((x, y)))
                                added_stone.draw()
                                board.update_liberties(added_stone)
                                if CHANGE:
                                    HUMAN_OR_AI = 'AI'
        elif HUMAN_OR_AI == 'AI':
            if mode == 'EVE':
                if board.next == BLACK:
                    if BLACK_AI_STRATEGY == 'RANDOM':
                        point = predict.random_point()
                    elif BLACK_AI_STRATEGY == 'MODEL':
                        x = deal_a_step(board)
                        point = predict.predict(model, x)
                elif board.next == WHITE:
                    if WHITE_AI_STRATEGY == 'RANDOM':
                        point = predict.random_point()
                    elif WHITE_AI_STRATEGY == 'MODEL':
                        x = deal_a_step(board)
                        point = predict.predict(model, x)
            else:
                x = deal_a_step(board)
                point = predict.predict(model, x)
            stone = board.search(point)
            if stone:
                pass
            else:
                fake_board = copy.deepcopy(board)
                fake_added_stone = Stone(fake_board, point, fake_board.turn(point))
                if not fake_board.is_legal(fake_added_stone):
                    pass
                else:
                    added_stone = Stone(board, point, board.turn(point))
                    added_stone.draw()
                    board.update_liberties(added_stone)
                    if CHANGE:
                        HUMAN_OR_AI = 'HUMAN'