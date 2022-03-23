import pygame
import os
from math import fabs
 
WHITE_PAWN_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'wp.png'))
WHITE_BISHOP_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'wb.png'))
WHITE_KNIGHT_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'wn.png'))
WHITE_ROOK_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'wr.png'))
WHITE_QUEEN_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'wq.png'))
WHITE_KING_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'wk.png'))
 
 
BLACK_PAWN_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'bp.png'))
BLACK_BISHOP_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'bb.png'))
BLACK_KNIGHT_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'bn.png'))
BLACK_ROOK_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'br.png'))
BLACK_QUEEN_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'bq.png'))
BLACK_KING_IMAGE = pygame.image.load(os.path.join('chess', 'chess_pieces', 'bk.png'))
 
 
 
 
class Piece:
    def __init__(self, team, image, value):
        self.team = team
        self.image = image
        self.value = value

    def is_pinned(self, board, row, col):
        pins = {
            "top_left" : self.is_pinned_top_left(board, row, col),
            "left" : self.is_pinned_left(board, row, col),
            "bottom left" : self.is_pinned_bottom_left(board, row, col),
            "bottom" : self.is_pinned_bottom(board, row, col),
            "bottom right" : self.is_pinned_bottom_right(board, row, col),
            "right" : self.is_pinned_right(board, row, col),
            "top right" : self.is_pinned_top_right(board, row, col),
            "top" : self.is_pinned_top(board, row, col)
        }
        if True in pins:
            return True
        else:
            return False

    def list_of_pins(self, board, row, col):
        pins = {
            "bottom-top": True in (self.is_pinned_bottom(board, row, col), self.is_attacked_top(board,row,col)),
            "BR-TL": True in (self.is_pinned_bottom_right(board, row, col), self.is_attacked_top_left(board,row,col)),
            "TR-BL": True in (self.is_pinned_top_right(board, row, col), self.is_attacked_bottom_left(board,row,col)),
            "left-right": True in (self.is_pinned_right(board, row, col), self.is_attacked_left(board,row,col))
        }
        return pins

    def is_attacked_top_left(self, board, row, col):
        for i in range(1, 8):
            if row - i in range(8) and col - i in range(8):
                if board[row - i][col - i] != 0:
                    if board[row - i][col - i].team != self.team and type(board[row - i][col - i]) in (Bishop, Queen):
                        return True
                    else:
                        return False
    
    def is_protecting_bottom_right(self, board, row, col):
        for i in range(1, 8):
            if row + i in range(8) and col + i in range(8):
                if board[row + i][col + i] != 0:
                    if board[row + i][col + i].team == self.team and type(board[row + i][col + i]) == King:
                        return True
                    else:
                        return False

    def is_pinned_top_left(self, board, row, col):
        if self.is_attacked_top_left(board, row, col) and self.is_protecting_bottom_right(board, row, col):
            return True

    def is_attacked_left(self, board, row, col):
        for i in range(1, 8):
            if col - i in range(8):
                if board[row][col - i] != 0:
                    if board[row][col - i].team != self.team and type(board[row][col - i]) in (Rook, Queen):
                        return True
                    else:
                        return False

    def is_protecting_right(self, board, row, col):
        for i in range(1, 8):
            if col + i in range(8):
                if board[row][col + i] != 0:
                    if board[row][col + i].team == self.team and type(board[row][col + i]) == King:
                        return True
                    else:
                        return False

    def is_pinned_left(self, board, row, col):
        if self.is_attacked_left(board, row, col) and self.is_protecting_right(board, row, col):
            return True

    def is_attacked_bottom_left(self, board, row, col):
        attacked = False
        for i in range(1, 8):
            if row + i in range(8) and col - i in range(8):
                if board[row + i][col - i] != 0:
                    if board[row + i][col - i].team != self.team and type(board[row + i][col - i]) in (Bishop, Queen):
                        attacked = True
                        break
        return attacked

    def is_protecting_top_right(self, board, row, col):
        for i in range(1, 8):
            if row - i in range(8) and col + i in range(8):
                if board[row - i][col + i] != 0:
                    if board[row - i][col + i].team == self.team and type(board[row - i][col + i]) == King:
                        return True
                    else:
                        return False

    def is_pinned_bottom_left(self, board, row, col):
        if self.is_attacked_bottom_left(board, row, col) and self.is_protecting_top_right(board, row, col):
            return True

    def is_attacked_bottom(self, board, row, col):
        for i in range(1, 8):
            if row +  i in range(8):
                if board[row + i][col] != 0:
                    if board[row + i][col].team != self.team and type(board[row + i][col]) in (Rook, Queen):
                        return True
                    else:
                        return False

    def is_protecting_top(self, board, row, col):
        for i in range(1, 8):
            if row - i in range(8):
                if board[row - i][col] != 0:
                    if board[row - i][col].team == self.team and type(board[row - i][col]) == King:
                        return True
                    else:
                        return False

    def is_pinned_bottom(self, board, row, col):
        if self.is_attacked_bottom(board, row, col) and self.is_protecting_top(board, row, col):
            return True

    def is_attacked_bottom_right(self, board, row, col):
        for i in range(1, 8):
            if row + i in range(8) and col + i in range(8):
                if board[row + i][col + i] != 0:
                    if board[row + i][col + i].team != self.team and type(board[row + i][col + i]) in (Bishop, Queen):
                        return True
                    else:
                        return False
    
    def is_protecting_top_left(self, board, row, col):
        for i in range(1, 8):
            if row - i in range(8) and col - i in range(8):
                if board[row - i][col - i] != 0:
                    if board[row - i][col - i].team == self.team and type(board[row - i][col - i]) == King:
                        return True
                    else:
                        return False

    def is_pinned_bottom_right(self, board, row, col):
        if self.is_attacked_bottom_right(board, row, col) and self.is_protecting_top_left(board, row, col):
            return True

    def is_attacked_right(self, board, row, col):
        for i in range(1, 8):
            if col + i in range(8):
                if board[row][col + i] != 0:
                    if board[row][col + i].team != self.team and type(board[row][col + i]) in (Rook, Queen):
                        return True
                    else:
                        return False

    def is_protecting_left(self, board, row, col):
        for i in range(1, 8):
            if col - i in range(8):
                if board[row][col - i] != 0:
                    if board[row][col - i].team == self.team and type(board[row][col - i]) == King:
                        return True
                    else:
                        return False
 
    def is_pinned_right(self, board, row, col):
        if self.is_attacked_right(board, row, col) and self.is_protecting_left(board, row, col):
            return True

    def is_attacked_top_right(self, board, row, col):
        for i in range(1, 8):
            if row - i in range(8) and col + i in range(8):
                if board[row - i][col + i] != 0:
                    if board[row - i][col + i].team != self.team and type(board[row - i][col + i]) in (Bishop, Queen):
                        return True
                    else:
                        return False

    def is_protecting_bottom_left(self, board, row, col):
        for i in range(1, 8):
            if row + i in range(8) and col - i in range(8):
                if board[row + i][col - i] != 0:
                    if board[row + i][col - i].team == self.team and type(board[row + i][col - i]) == King:
                        return True
                    else:
                        return False

    def is_pinned_top_right(self, board, row, col):
        if self.is_attacked_top_right(board, row, col) and self.is_protecting_bottom_left(board, row, col):
            return True

    def is_attacked_top(self, board, row, col):
        for i in range(1, 8):
            if row - i in range(8):
                if board[row - i][col] != 0:
                    if board[row - i][col].team != self.team and type(board[row - i][col]) in (Rook, Queen):
                        return True
                    else:
                        return False

    def is_protecting_bottom(self, board, row, col):
        for i in range(1, 8):
            if row +  i in range(8):
                if board[row + i][col] != 0:
                    if board[row + i][col].team == self.team and type(board[row + i][col]) == King:
                        return True
                    else:
                        return False

    def is_pinned_top(self, board, row, col):
        if self.is_attacked_top(board, row, col) and self.is_protecting_bottom(board, row, col):
            return True


class Pawn(Piece):
    def possible_moves_list(self, board, row, col):
        possible_moves = []
        if self.team == 0:
            if board[row - 1][col] == 0 and row > 0:
                possible_moves.append([row -1, col])
                if board[row - 2][col] == 0 and row == 6:
                    possible_moves.append([row - 2, col])
            if col > 0 and board[row - 1][col - 1] != 0 and board[row - 1][col - 1].team != self.team:
                    possible_moves.append([row - 1, col - 1])
            if col < 7 and board[row - 1][col + 1] != 0 and board[row - 1][col + 1].team != self.team:
                    possible_moves.append([row - 1, col + 1])
            if col < 7 and board[row - 1][col + 1] == 0 and row == 3 and type(board[row][col + 1]) == Pawn:
                    possible_moves.append([row - 1, col + 1])

        if self.team == 1:
            if board[row + 1][col] == 0 and row < 7:
                possible_moves.append([row + 1, col])
                if board[row + 2][col] == 0 and row == 1:
                    possible_moves.append([row + 2, col])
            if col > 0 and board[row + 1][col - 1] != 0 and board[row + 1][col - 1].team != self.team:
                possible_moves.append([row + 1, col - 1])
            if col < 7 and board[row + 1][col + 1] != 0 and board[row + 1][col + 1].team != self.team:
                possible_moves.append([row + 1, col + 1])
            #en pessant
            if col > 0 and board[row + 1][col - 1] == 0 and row == 4 and type(board[row][col - 1]) == Pawn:
                possible_moves.append([row + 1, col - 1])
            if col < 7 and board[row + 1][col + 1] == 0 and row == 4 and type(board[row][col + 1]) == Pawn:
                possible_moves.append([row + 1, col + 1])

        return possible_moves
 
class Knight(Piece):
    def possible_moves_list(self, board, row, col):
        possible_moves = []
        for i in [-1, -2, 1, 2]:
            for j in [-1, -2, 1, 2]:
                if fabs(i) != fabs(j) and row + i in range(8) and col + j in range(8):
                    if board[row + i][col + j] == 0 or board[row + i][col + j].team != self.team:
                        possible_moves.append([row + i, col + j])
        return possible_moves
 
class Bishop(Piece):
    def possible_moves_list(self, board, row, col):
        possible_moves = []
        #top left moves
        for i in range(1, 7):
            if row - i >= 0 and col - i >= 0:
                if board[row - i][col - i] == 0:
                    possible_moves.append([row - i, col - i])
                elif board[row - i][col - i].team != self.team:
                    possible_moves.append([row - i, col - i])
                    break
                else:
                    break
        #top right moves
        for i in range(1, 7):
            if row - i >= 0 and col + i <= 7:
                if board[row - i][col + i] == 0:
                    possible_moves.append([row - i, col + i])
                elif board[row - i][col + i].team != self.team:
                    possible_moves.append([row - i, col + i])
                    break
                else:
                    break
        #bottom right moves
        for i in range(1, 7):
            if row + i <= 7 and col + i <= 7:
                if board[row + i][col + i] == 0:
                    possible_moves.append([row + i, col + i])
                elif board[row + i][col + i].team != self.team:
                    possible_moves.append([row + i, col + i])
                    break
                else:
                    break
        #bottom left moves
        for i in range(1, 7):
            if row + i <= 7 and col - i >= 0:
                if board[row + i][col - i] == 0:
                    possible_moves.append([row + i, col - i])
                elif board[row + i][col - i].team != self.team:
                    possible_moves.append([row + i, col - i])
                    break
                else:
                    break
        return possible_moves
 
class Rook(Piece):
    moved = False
    def has_moved(self):
        return self.moved
    def move(self):
        self.moved = True
    def possible_moves_list(self, board, row, col):
        possible_moves = []
        #top move
        for i in range(1, 7):
            if row - i >= 0:
                if board[row - i][col] == 0:
                    possible_moves.append([row - i, col])
                elif board[row - i][col].team != self.team:
                    possible_moves.append([row - i, col])
                    break
                else:
                    break
        #right move
        for i in range(1, 7):
            if col + i <= 7:
                if board[row][col + i] == 0:
                    possible_moves.append([row, col + i])
                elif board[row][col + i].team != self.team:
                    possible_moves.append([row, col + i])
                    break
                else:
                    break
        #bottom move
        for i in range(1, 7):
            if row + i <= 7:
                if board[row + i][col] == 0:
                    possible_moves.append([row + i, col])
                elif board[row + i][col].team != self.team:
                    possible_moves.append([row + i, col])
                    break
                else:
                    break
        #left move
        for i in range(1, 7):
            if col - i >= 0:
                if board[row][col - i] == 0:
                    possible_moves.append([row, col - i])
                elif board[row][col - i].team != self.team:
                    possible_moves.append([row, col - i])
                    break
                else:
                    break
        return possible_moves

 
class Queen(Piece):
    def possible_moves_list(self, board, row, col):
        possible_moves = []
       #top left moves
        for i in range(1, 7):
            if row - i >= 0 and col - i >= 0:
                if board[row - i][col - i] == 0:
                    possible_moves.append([row - i, col - i])
                elif board[row - i][col - i].team != self.team:
                    possible_moves.append([row - i, col - i])
                    break
                else:
                    break
        #top right moves
        for i in range(1, 7):
            if row - i >= 0 and col + i <= 7:
                if board[row - i][col + i] == 0:
                    possible_moves.append([row - i, col + i])
                elif board[row - i][col + i].team != self.team:
                    possible_moves.append([row - i, col + i])
                    break
                else:
                    break
        #bottom right moves
        for i in range(1, 7):
            if row + i <= 7 and col + i <= 7:
                if board[row + i][col + i] == 0:
                    possible_moves.append([row + i, col + i])
                elif board[row + i][col + i].team != self.team:
                    possible_moves.append([row + i, col + i])
                    break
                else:
                    break
        #bottom left moves
        for i in range(1, 7):
            if row + i <= 7 and col - i >= 0:
                if board[row + i][col - i] == 0:
                    possible_moves.append([row + i, col - i])
                elif board[row + i][col - i].team != self.team:
                    possible_moves.append([row + i, col - i])
                    break
                else:
                    break
        #top move
        for i in range(1, 7):
            if row - i >= 0:
                if board[row - i][col] == 0:
                    possible_moves.append([row - i, col])
                elif board[row - i][col].team != self.team:
                    possible_moves.append([row - i, col])
                    break
                else:
                    break
        #right move
        for i in range(1, 7):
            if col + i <= 7:
                if board[row][col + i] == 0:
                    possible_moves.append([row, col + i])
                elif board[row][col + i].team != self.team:
                    possible_moves.append([row, col + i])
                    break
                else:
                    break
        #bottom move
        for i in range(1, 7):
            if row + i <= 7:
                if board[row + i][col] == 0:
                    possible_moves.append([row + i, col])
                elif board[row + i][col].team != self.team:
                    possible_moves.append([row + i, col])
                    break
                else:
                    break
        #left move
        for i in range(1, 7):
            if col - i >= 0:
                if board[row][col - i] == 0:
                    possible_moves.append([row, col - i])
                elif board[row][col - i].team != self.team:
                    possible_moves.append([row, col - i])
                    break
                else:
                    break
        return possible_moves
 
class King(Piece):
    moved = False
    def move(self):
        self.moved = True
    def has_moved(self):
        return self.moved
    def possible_moves_list(self, board, row, col):
        possible_moves = []
        for i in [-1, 1]:
            if row + i in range(0, 8):
                if board[row + i][col] == 0 or board[row + i][col].team != self.team:
                    possible_moves.append([row + i, col])
            if col + i in range(0, 8):
                if board[row][col + i] == 0 or board[row][col + i].team != self.team:
                    possible_moves.append([row, col + i])
            for j in [-1, 1]:
                if row + i in range(0, 8) and col + i in range(0, 8):
                    if board[row + i][col + i] == 0 or board[row + i][col + i].team != self.team:
                        possible_moves.append([row + i, col + j])
        #castle short
        if not self.has_moved():
            squares_are_empty = True
            for i in range(1, 3):
                    squares_are_empty = False
                    break
            if squares_are_empty and type(board[row][col + 3]) == Rook and not board[row][col + 3].has_moved():
                possible_moves.append([row, col + 2])
            #castle long
            squares_are_empty = True
            for i in range(1, 4):
                if board[row][col - i] != 0:
                    squares_are_empty = False
                    break
            if squares_are_empty and type(board[row][col - 4]) == Rook and not board[row][col - 4].has_moved():
                possible_moves.append([row, col - 2])
        return possible_moves

    def is_in_double_check(self, board, row, col):
        checks = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0 and board[i][j].team != self.team and [row, col] in board[i][j].possible_moves_list(board, i, j):
                    checks += 1
        return checks > 1

    def is_in_single_check(self, board, row, col):
        check = False
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0 and board[i][j].team != self.team and [row, col] in board[i][j].possible_moves_list(board, i, j):
                    check = True
                    break
        return (check, i, j)