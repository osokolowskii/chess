import pygame
import os
 
WHITE_PAWN_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'wp.png'))
WHITE_BISHOP_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'wb.png'))
WHITE_KNIGHT_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'wn.png'))
WHITE_ROOK_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'wr.png'))
WHITE_QUEEN_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'wq.png'))
WHITE_KING_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'wk.png'))
 
 
BLACK_PAWN_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'bp.png'))
BLACK_BISHOP_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'bb.png'))
BLACK_KNIGHT_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'bn.png'))
BLACK_ROOK_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'br.png'))
BLACK_QUEEN_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'bq.png'))
BLACK_KING_IMAGE = pygame.image.load(os.path.join('chess', 'chess pieces', 'bk.png'))
 
 
 
 
class Piece:
    def __init__(self, team, image, value):
        self.team = team
        self.image = image
        self.value = value
 
class Pawn(Piece):
    def possible_moves_list(self, board, startRow, startCol):
        possible_moves = []
        if self.team == 0:
            if board[startRow - 1][startCol] == 0 and startRow > 0:
                possible_moves.append([startRow -1, startCol])
                if board[startRow - 2][startCol] == 0 and startRow == 6:
                    possible_moves.append([startRow - 2, startCol])
            if startCol > 0 and board[startRow - 1][startCol - 1] != 0 and board[startRow - 1][startCol - 1].team != self.team:
                possible_moves.append([startRow - 1, startCol - 1])
            if startCol < 7 and board[startRow - 1][startCol + 1] != 0 and board[startRow - 1][startCol + 1].team != self.team:
                possible_moves.append([startRow - 1, startCol + 1])
            #en pessant
            if startCol > 0 and board[startRow - 1][startCol - 1] == 0 and startRow == 3 and type(board[startRow][startCol - 1]) == Pawn:
                possible_moves.append([startRow - 1, startCol - 1])
            if startCol < 7 and board[startRow - 1][startCol + 1] == 0 and startRow == 3 and type(board[startRow][startCol + 1]) == Pawn:
                possible_moves.append([startRow - 1, startCol + 1])

        if self.team == 1:
            if board[startRow + 1][startCol] == 0 and startRow < 7:
                possible_moves.append([startRow + 1, startCol])
                if board[startRow + 2][startCol] == 0 and startRow == 1:
                    possible_moves.append([startRow + 2, startCol])
            if startCol > 0 and board[startRow + 1][startCol - 1] != 0 and board[startRow + 1][startCol - 1].team != self.team:
                possible_moves.append([startRow + 1, startCol - 1])
            if startCol < 7 and board[startRow + 1][startCol + 1] != 0 and board[startRow + 1][startCol + 1].team != self.team:
                possible_moves.append([startRow + 1, startCol + 1])
            #en pessant
            if startCol > 0 and board[startRow + 1][startCol - 1] == 0 and startRow == 4 and type(board[startRow][startCol - 1]) == Pawn:
                possible_moves.append([startRow + 1, startCol - 1])
            if startCol < 7 and board[startRow + 1][startCol + 1] == 0 and startRow == 4 and type(board[startRow][startCol + 1]) == Pawn:
                possible_moves.append([startRow + 1, startCol + 1])

        return possible_moves
 
class Knight(Piece):
    def possible_moves_list(self, board, startRow, startCol):
        possible_moves = []
        for i in [-1, -2, 1, 2]:
            for j in [-1, -2, 1, 2]:
                if i + j != 0 and i + j != 2 * i and startRow + i in range(8) and startCol + j in range(8):
                    if board[startRow + i][startCol + j] == 0 or board[startRow + i][startCol + j].team != self.team:
                        possible_moves.append([startRow + i, startCol + j])
        return possible_moves
 
class Bishop(Piece):
    def possible_moves_list(self, board, startRow, startCol):
        possible_moves = []
        #top left moves
        for i in range(1, 7):
            if startRow - i >= 0 and startCol - i >= 0:
                if board[startRow - i][startCol - i] == 0:
                    possible_moves.append([startRow - i, startCol - i])
                elif board[startRow - i][startCol - i].team != self.team:
                    possible_moves.append([startRow - i, startCol - i])
                    break
                else:
                    break
        #top right moves
        for i in range(1, 7):
            if startRow - i >= 0 and startCol + i <= 7:
                if board[startRow - i][startCol + i] == 0:
                    possible_moves.append([startRow - i, startCol + i])
                elif board[startRow - i][startCol + i].team != self.team:
                    possible_moves.append([startRow - i, startCol + i])
                    break
                else:
                    break
        #down right moves
        for i in range(1, 7):
            if startRow + i <= 7 and startCol + i <= 7:
                if board[startRow + i][startCol + i] == 0:
                    possible_moves.append([startRow + i, startCol + i])
                elif board[startRow + i][startCol + i].team != self.team:
                    possible_moves.append([startRow + i, startCol + i])
                    break
                else:
                    break
        #down left moves
        for i in range(1, 7):
            if startRow + i <= 7 and startCol - i >= 0:
                if board[startRow + i][startCol - i] == 0:
                    possible_moves.append([startRow + i, startCol - i])
                elif board[startRow + i][startCol - i].team != self.team:
                    possible_moves.append([startRow + i, startCol - i])
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
    def possible_moves_list(self, board, startRow, startCol):
        possible_moves = []
        #top move
        for i in range(1, 7):
            if startRow - i >= 0:
                if board[startRow - i][startCol] == 0:
                    possible_moves.append([startRow - i, startCol])
                elif board[startRow - i][startCol].team != self.team:
                    possible_moves.append([startRow - i, startCol])
                    break
                else:
                    break
        #right move
        for i in range(1, 7):
            if startCol + i <= 7:
                if board[startRow][startCol + i] == 0:
                    possible_moves.append([startRow, startCol + i])
                elif board[startRow][startCol + i].team != self.team:
                    possible_moves.append([startRow, startCol + i])
                    break
                else:
                    break
        #down move
        for i in range(1, 7):
            if startRow + i <= 7:
                if board[startRow + i][startCol] == 0:
                    possible_moves.append([startRow + i, startCol])
                elif board[startRow + i][startCol].team != self.team:
                    possible_moves.append([startRow + i, startCol])
                    break
                else:
                    break
        #left move
        for i in range(1, 7):
            if startCol - i >= 0:
                if board[startRow][startCol - i] == 0:
                    possible_moves.append([startRow, startCol - i])
                elif board[startRow][startCol - i].team != self.team:
                    possible_moves.append([startRow, startCol - i])
                    break
                else:
                    break
        return possible_moves

 
class Queen(Piece):
    def possible_moves_list(self, board, startRow, startCol):
        possible_moves = []
       #top left moves
        for i in range(1, 7):
            if startRow - i >= 0 and startCol - i >= 0:
                if board[startRow - i][startCol - i] == 0:
                    possible_moves.append([startRow - i, startCol - i])
                elif board[startRow - i][startCol - i].team != self.team:
                    possible_moves.append([startRow - i, startCol - i])
                    break
                else:
                    break
        #top right moves
        for i in range(1, 7):
            if startRow - i >= 0 and startCol + i <= 7:
                if board[startRow - i][startCol + i] == 0:
                    possible_moves.append([startRow - i, startCol + i])
                elif board[startRow - i][startCol + i].team != self.team:
                    possible_moves.append([startRow - i, startCol + i])
                    break
                else:
                    break
        #down right moves
        for i in range(1, 7):
            if startRow + i <= 7 and startCol + i <= 7:
                if board[startRow + i][startCol + i] == 0:
                    possible_moves.append([startRow + i, startCol + i])
                elif board[startRow + i][startCol + i].team != self.team:
                    possible_moves.append([startRow + i, startCol + i])
                    break
                else:
                    break
        #down left moves
        for i in range(1, 7):
            if startRow + i <= 7 and startCol - i >= 0:
                if board[startRow + i][startCol - i] == 0:
                    possible_moves.append([startRow + i, startCol - i])
                elif board[startRow + i][startCol - i].team != self.team:
                    possible_moves.append([startRow + i, startCol - i])
                    break
                else:
                    break
        #top move
        for i in range(1, 7):
            if startRow - i >= 0:
                if board[startRow - i][startCol] == 0:
                    possible_moves.append([startRow - i, startCol])
                elif board[startRow - i][startCol].team != self.team:
                    possible_moves.append([startRow - i, startCol])
                    break
                else:
                    break
        #right move
        for i in range(1, 7):
            if startCol + i <= 7:
                if board[startRow][startCol + i] == 0:
                    possible_moves.append([startRow, startCol + i])
                elif board[startRow][startCol + i].team != self.team:
                    possible_moves.append([startRow, startCol + i])
                    break
                else:
                    break
        #down move
        for i in range(1, 7):
            if startRow + i <= 7:
                if board[startRow + i][startCol] == 0:
                    possible_moves.append([startRow + i, startCol])
                elif board[startRow + i][startCol].team != self.team:
                    possible_moves.append([startRow + i, startCol])
                    break
                else:
                    break
        #left move
        for i in range(1, 7):
            if startCol - i >= 0:
                if board[startRow][startCol - i] == 0:
                    possible_moves.append([startRow, startCol - i])
                elif board[startRow][startCol - i].team != self.team:
                    possible_moves.append([startRow, startCol - i])
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
    def possible_moves_list(self, board, startRow, startCol):
        possible_moves = []
        for i in [-1, 1]:
            if startRow + i in range(0, 8):
                if board[startRow + i][startCol] == 0 or board[startRow + i][startCol].team != self.team:
                    possible_moves.append([startRow + i, startCol])
            if startCol + i in range(0, 8):
                if board[startRow][startCol + i] == 0 or board[startRow][startCol + i].team != self.team:
                    possible_moves.append([startRow, startCol + i])
            for j in [-1, 1]:
                if startRow + i in range(0, 8) and startCol + i in range(0, 8):
                    if board[startRow + i][startCol + i] == 0 or board[startRow + i][startCol + i].team != self.team:
                        possible_moves.append([startRow + i, startCol + j])
        #castle short
        if not self.has_moved():
            squares_are_empty = True
            for i in range(1, 3):
                    squares_are_empty = False
                    break
            if squares_are_empty and type(board[startRow][startCol + 3]) == Rook and not board[startRow][startCol + 3].has_moved():
                possible_moves.append([startRow, startCol + 2])
            #castle long
            squares_are_empty = True
            for i in range(1, 4):
                if board[startRow][startCol - i] != 0:
                    squares_are_empty = False
                    break
            if squares_are_empty and type(board[startRow][startCol - 4]) == Rook and not board[startRow][startCol - 4].has_moved():
                possible_moves.append([startRow, startCol - 2])
        return possible_moves