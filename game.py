from pieces import *
from math import fabs

class Game:
    king_positions = [[7, 4], [0, 4]]
    last_move = [0, 0]
    team_on_move = 0
    opposite_team = 1

    def square_is_attacked(self, board, team, row, col):
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0 and board[i][j].team == team:
                    if[row, col] in board[i][j].possible_moves_list(board, i, j) and type(board[i][j]) != Pawn:
                            return True
                    if type(board[i][j]) == Pawn and col in (j + 1, j - 1):
                        if team == 0 and i - 1 == row or team == 1 and i + 1 == row:
                            return True
    
    def possible_moves_list(self, board, team, moves_list):
        '''return value of this function is a list of all possible moves, which are presented in the form of a list( [starting_row, starting_col, ending_row, ending_col] )'''
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0 and board[i][j].team == team:
                    for move in board[i][j].possible_moves_list(board, i, j):
                        moves_list.append([i, j, *move])

    def handle_double_check(self, king_row, king_col, moves_list):
        '''this function removes every moves by pieces other than king'''
        indexes_to_remove = []
        for move in moves_list:
                if move[0] != king_row or move[1] != king_col:
                    indexes_to_remove.append(moves_list.index(move))
        return [x for x in moves_list if not moves_list.index(x) in indexes_to_remove]

    def checking_piece_location(self, board, king_row, king_col, team):
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0 and board[i][j].team == team and [king_row, king_col] in board[i][j].possible_moves_list(board, i, j):
                    return [i, j]

    def handle_single_check(self, board, king_row, king_col, checking_piece_location, moves_list):
        '''If pawn or knight gives check, other pieces than king can only capture them - they can't cover the king from attack by these pieces.
        if check is given by rook, bishop or queen, non-king pieces can either capture that piece or stand between the king and that piece, covering king from attack
        algorithm at lines DOKONCZ'''
        indexes_to_remove = []
        possible_squares = []
        if type(board[checking_piece_location[0]][checking_piece_location[1]]) in (Pawn, Knight):
            possible_squares.append([checking_piece_location[0], checking_piece_location[1]])
        else:
            if king_row != checking_piece_location[0]:
                difference = int(fabs(king_row - checking_piece_location[0]))
            else:
                difference = int(fabs(king_col - checking_piece_location[1]))
            if board[king_row][king_col].is_attacked_top_left(board, king_row, king_col):
                for i in range(1, difference + 1):
                    possible_squares.append([king_row - i, king_col - i])
            elif board[king_row][king_col].is_attacked_left(board, king_row, king_col):
                for i in range(1, difference + 1):
                    possible_squares.append([king_row, king_col - i])
            elif board[king_row][king_col].is_attacked_bottom_left(board, king_row, king_col):
                for i in range(1, difference + 1):
                    possible_squares.append([king_row + i, king_col - i])
            elif board[king_row][king_col].is_attacked_bottom(board, king_row, king_col):
                for i in range(1, difference + 1):
                    possible_squares.append([king_row + i, king_col])
            elif board[king_row][king_col].is_attacked_bottom_right(board, king_row, king_col):
                for i in range(1, difference + 1):
                    possible_squares.append([king_row + i, king_col + i])
            elif board[king_row][king_col].is_attacked_right(board, king_row, king_col):
                for i in range(1, difference + 1):
                    possible_squares.append([king_row, king_col + i])
            elif board[king_row][king_col].is_attacked_top_right(board, king_row, king_col):
                for i in range(1, difference + 1):
                    possible_squares.append([king_row - i, king_col + i])
            else:
                for i in range(1, difference + 1):
                    possible_squares.append([king_row - i, king_col])
        for move in moves_list:
            if type(board[move[0]][move[1]]) != King:
                if [move[2], move[3]] not in possible_squares:
                    indexes_to_remove.append(moves_list.index(move))
        return [x for x in moves_list if not moves_list.index(x) in indexes_to_remove]

    def handle_king_moves(self, board, king_row, king_col, moves_list):
        indexes_to_remove = []
        for move in moves_list:
            if move[0] == king_row and move[1] == king_col:
                if self.square_is_attacked(board, self.opposite_team, move[2], move[3]):
                    indexes_to_remove.append(moves_list.index(move))
                elif board[king_row][king_col].is_attacked_top_left(board, king_row, king_col) and move[2] > king_row and move[3] < king_col:
                    indexes_to_remove.append(moves_list.index(move))
                elif board[king_row][king_col].is_attacked_left(board, king_row, king_col) and move[2] == king_row and move[3] < king_col:
                    indexes_to_remove.append(moves_list.index(move))
                elif board[king_row][king_col].is_attacked_bottom_left(board, king_row, king_col) and move[2] < king_row and move[3] < king_col:
                    indexes_to_remove.append(moves_list.index(move))
                elif board[king_row][king_col].is_attacked_bottom(board, king_row, king_col) and move[2] < king_row and move[3] == king_col:
                    indexes_to_remove.append(moves_list.index(move))
                elif board[king_row][king_col].is_attacked_bottom_right(board, king_row, king_col) and move[2] < king_row and move[3] > king_col:
                    indexes_to_remove.append(moves_list.index(move))
                elif board[king_row][king_col].is_attacked_right(board, king_row, king_col) and move[2] == king_row and move[3] < king_col:
                    indexes_to_remove.append(moves_list.index(move))
                elif board[king_row][king_col].is_attacked_top_right(board, king_row, king_col) and move[2] < king_row and move[3] > king_col:
                    indexes_to_remove.append(moves_list.index(move))
                elif board[king_row][king_col].is_attacked_top(board, king_row, king_col) and move[2] < king_row and move[3] == king_col:
                    indexes_to_remove.append(moves_list.index(move))
        return [x for x in moves_list if not moves_list.index(x) in indexes_to_remove]

    def handle_pins(self, board, moves_list):
        indexes_to_remove = []
        for move in moves_list:
            if type(board[move[0]][move[1]]) != King and board[move[0]][move[1]].is_pinned(board, move[0], move[1]):
                if type(board[move[0]][move[1]]) == Knight:
                    indexes_to_remove.append(moves_list.index(move))
                else:
                    list_of_pins = board[move[0]][move[1]].list_of_pins(board, move[0], move[1])
                    if list_of_pins["bottom-top"] and move[1] != move[3]:
                        indexes_to_remove.append(moves_list.index(move))
                    elif list_of_pins["left-right"] and move[0] != move[2]:
                        indexes_to_remove.append(moves_list.index(move))
                    elif list_of_pins["BR-TL"]:
                        if move[0] > move[2] and move[1] < move[3] or move[0] < move[2] and move[1] > move[3] or move[0] == move[2] or move[1] == move[3]:
                            indexes_to_remove.append(moves_list.index(move))
                    elif list_of_pins["TR-BL"]:
                        if move[0] > move[2] and move[1] > move[3] or move[0] < move[2] and move[1] < move[3] or move[0] == move[2] or move[1] == move[3]:
                            indexes_to_remove.append(moves_list.index(move))
        return [x for x in moves_list if not moves_list.index(x) in indexes_to_remove]

    def handle_en_pessant(self, board, moves_list):
        indexes_to_remove = []
        for move in moves_list:
            if type(board[move[0]][move[1]]) == Pawn and move[1] != move[3] and board[move[2]][move[3]] == 0:
                if self.last_move != [move[0], move[3]]:
                    indexes_to_remove.append(moves_list.index(move))
        return [x for x in moves_list if not moves_list.index(x) in indexes_to_remove]

    def list_of_legal_moves(self, board):
        '''this function removes every pseudo legal move - move that is possible for piece or pawn but puts their own king in check or do not handle with check already given.
        when king is under double check only king can move - any other move do not handle this type of check. if king is under single check - king can move to safe square or
        other piece can capture checking piece or cover their king (if checking piece is not pawn or knight'''
        moves_list = []
        self.possible_moves_list(board, self.team_on_move, moves_list)
        king_row = self.king_positions[self.team_on_move][0]
        king_col = self.king_positions[self.team_on_move][1]
        if board[king_row][king_col].is_in_double_check(board, king_row, king_col):
            moves_list = self.handle_double_check(king_row, king_col, moves_list)
        elif board[king_row][king_col].is_in_single_check(board, king_row, king_col):
            moves_list = self.handle_single_check(board, king_row, king_col, self.checking_piece_location(board, king_row, king_col, self.opposite_team), moves_list)
        moves_list = self.handle_king_moves(board, king_row, king_col, moves_list)
        moves_list = self.handle_pins(board, moves_list)
        moves_list = self.handle_en_pessant(board, moves_list)
        return moves_list

    def promote(self, board, row, col):
        print('Which piece you want to promote pawn to? Type q/r/n/b (letters stands for: queen, rook, knight and bishop)')
        while True:
            promoting_piece = input(" ")
            match promoting_piece:
                case 'q':
                    if row == 0:
                        board[row][col] = Queen(0, WHITE_QUEEN_IMAGE, 9)
                    else:
                        board[row][col] = Queen(1, BLACK_QUEEN_IMAGE, 9)
                    break
                case 'r':
                    if row == 0:
                        board[row][col] = Rook(0, WHITE_ROOK_IMAGE, 5)
                    else:
                        board[row][col] = Rook(1, BLACK_ROOK_IMAGE, 5)
                    break
                case 'n':
                    if row == 0:
                        board[row][col] = Knight(0, WHITE_KNIGHT_IMAGE, 3)
                    else:
                        board[row][col] = Knight(1, BLACK_KNIGHT_IMAGE, 3)
                    break
                case 'b':
                    if row == 0:
                        board[row][col] = Bishop(0, WHITE_BISHOP_IMAGE, 3)
                    else:
                        board[row][col] = Bishop(1, BLACK_BISHOP_IMAGE, 3)
                    break
                case _:
                    print('invalid input')

    def make_move(self, board, start_row, start_col, end_row, end_col):
        if [start_row, start_col, end_row, end_col] in self.list_of_legal_moves(board):
            if type(board[start_row][start_col]) == King and end_col in (start_col + 2, start_col - 2):
                if end_col > start_col:
                    board[start_row][5] = board[start_row][7]
                    board[start_row][7] = 0
                    board[start_row][5].move()
                else:
                    board[start_row][3] = board[start_row][0]
                    board[start_row][0] = 0
                    board[start_row][3].move()
            elif type(board[start_row][start_col]) == Pawn and end_col != start_col and board[end_row][end_col] == 0:
                board[start_row][end_col] = 0
            board[end_row][end_col] = board[start_row][start_col]
            board[start_row][start_col] = 0
            if type(board[end_row][end_col]) == King:
                self.king_positions[self.team_on_move] = [end_row, end_col]
            if self.team_on_move == 0:
                self.team_on_move = 1
                self.opposite_team = 0
            else:
                self.team_on_move = 0
                self.opposite_team = 1
        self.last_move = [end_row, end_col]
        if type(board[end_row][end_col]) in (Rook, King) and not board[end_row][end_col].moved:
            board[end_row][end_col].move()
        if type(board[end_row][end_col]) == Pawn and end_row in (0, 7):
            self.promote(board, end_row, end_col)