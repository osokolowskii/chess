import pygame
from constants import *
from pieces import *
from board import *
from game import *
import time


pygame.init()



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('chess game')

wp = Pawn(0, WHITE_PAWN_IMAGE, 1)
wb = Bishop(0, WHITE_BISHOP_IMAGE, 3)
wn = Knight(0, WHITE_KNIGHT_IMAGE, 3)
wr = Rook(0, WHITE_ROOK_IMAGE, 5)
wq = Queen(0, WHITE_QUEEN_IMAGE, 9)
wk = King(0, WHITE_KING_IMAGE, 0)

bp = Pawn(1, BLACK_PAWN_IMAGE, 1)
bb = Bishop(1, BLACK_BISHOP_IMAGE, 3)
bn = Knight(1, BLACK_KNIGHT_IMAGE, 3)
br = Rook(1, BLACK_ROOK_IMAGE, 5)
bq = Queen(1, BLACK_QUEEN_IMAGE, 9)
bk = King(1, BLACK_KING_IMAGE, 0)

board = Board()

game = Game()

pieces_list = [wr, wn, wb, wq, wk, wp, bp, br, bn, bb, bq, bk]

def draw_board():
    WIN.fill(BROWN, (0, 0, 720, 720))
    for row in range (ROWS):
        for col in range (COLS):
            if row % 2 == 0:
                if col % 2 == 0:
                    pygame.draw.rect(WIN, WHITE, (SQUARE_SIZE * col, SQUARE_SIZE * row, SQUARE_SIZE, SQUARE_SIZE))
            elif row % 2 != 0:
                if col % 2 != 0:
                    pygame.draw.rect(WIN, WHITE, (SQUARE_SIZE * col, SQUARE_SIZE * row, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                WIN.blit(board[i][j].image, (SQUARE_SIZE * j, SQUARE_SIZE * i))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    board.set_start_position(pieces_list)
    while run:
        clock.tick(FPS)
        if game.result != None:
            game.print_result()
            time.sleep(3)
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x1, y1 = x // 90, y // 90                                                                           
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                x2, y2 = x // 90, y // 90                                                                    
                game.make_move(board.board, y1, x1, y2, x2)

        draw_pieces(board.board)
        draw_board()
    pygame.quit()
        

if __name__ == "__main__":
    main()