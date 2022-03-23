from pieces import Pawn, Knight, King

class Game:
    king_positions = [[7, 4], [0, 4]]
    last_move = [0, 0]
    team_on_move = 0
    opposite_team = 1

    def square_is_attacked(self, board, team, row, col):
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0 and board[i][j].team == team and [row, col] in board[i][j].possible_moves_list(board, i, j):
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
        for move in moves_list:
                if move[0] != king_row or move[1] != king_col:
                    moves_list.remove(move)

    def handle_single_check(self, board, king_row, king_col, checking_piece_location, moves_list):
        '''If pawn or knight gives check, other pieces than king can only capture them - they can't cover the king from attack by these pieces.
        if check is given by rook, bishop or queen non-king pieces can either capture that piece or stand between the king and that piece, covering king from attack
        algorithm at lines 49-65 count at which row and which column pieces can end their move to capture/cover checking piece.'''
        if type(board[checking_piece_location[0]][checking_piece_location[1]]) in (Pawn, Knight):
            for move in moves_list:
                if type(board[move[0][move[1]]]) != King and [move[2], move[3]] != checking_piece_location:
                    moves_list.remove(move)
        else:
            possible_rows = possible_cols = []
            if king_row - checking_piece_location[0] > 0:
                for i in range(checking_piece_location[0], king_row):
                    possible_rows.append(i)
            else:
                for i in range(king_row, checking_piece_location[0]):
                    possible_rows.append(i)
            if king_col - checking_piece_location[1] > 0:
                for i in range(checking_piece_location[1], king_col):
                    possible_cols.append(i)
            else:
                for i in range(king_col, checking_piece_location[1]):
                    possible_cols.append(i)
            for move in moves_list:
                if type(board[move[0]][move[1]]) != King and move[2] not in possible_rows or move[3] not in possible_cols:
                    moves_list.remove(move)

    def handle_king_moves(self, board, king_row, king_col, moves_list):
        for move in moves_list:
            if move[0] == king_row and move[1] == king_col:
                if self.square_is_attacked(board, self.opposite_team, move[2], move[3]):
                    moves_list.remove(move)

    def handle_pins(self, board, moves_list):
        for move in moves_list:
            if type(board[move[0]][move[1]]) != King and board[move[0]][move[1]].is_pinned(board, move[0], move[1]):
                if type(board[move[0]][move[1]]) == Knight:
                    moves_list.remove(move)
                else:
                    list_of_pins = board[move[0]][move[1]].list_of_pins(board, move[0], move[1])
                    if list_of_pins["bottom-top"] and move[1] != move[3]:
                        moves_list.remove(move)
                    elif list_of_pins["left-right"] and move[0] != move[2]:
                        moves_list.remove(move)
                    elif list_of_pins["BR-TL"]:
                        if move[0] > move[2] and move[1] < move[3] or move[0] < move[2] and move[1] > move[3] or move[0] == move[2] or move[1] == move[3]:
                            moves_list.remove(move)
                    elif list_of_pins["TR-BL"]:
                        if move[0] > move[2] and move[1] > move[3] or move[0] < move[2] and move[1] < move[3] or move[0] == move[2] or move[1] == move[3]:
                            moves_list.remove(move)

    def list_of_legal_moves(self, board):
        '''this function removes every pseudo legal move - move that is possible for piece or pawn but puts their own king in check or do not handle with check already given.
        when king is under double check only king can move - any other move do not handle this type of check. if king is under single check - king can move to safe square or
        other piece can capture checking piece or cover their king (if checking piece is not pawn or knight'''
        moves_list = []
        self.possible_moves_list(board, self.team_on_move, moves_list)
        king_row = self.king_positions[self.team_on_move][0]
        king_col = self.king_positions[self.team_on_move][1]
        single_check = board[king_row][king_col].is_in_single_check(board, king_row, king_col)
        if board[king_row][king_col].is_in_double_check(board, king_row, king_col):
            self.handle_double_check(king_row, king_col, moves_list)
        elif single_check[0]:
            checking_piece_location = [single_check[1], single_check[2]]
            self.handle_single_check(board, king_row, king_col, checking_piece_location, moves_list)
        self.handle_king_moves(board, king_row, king_col, moves_list)
        self.handle_pins(board, moves_list)
        return moves_list

    def make_move(self, board, start_row, start_col, end_row, end_col):
        if [start_row, start_col, end_row, end_col] in self.list_of_legal_moves(board):
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
        if board[2][2] != 0:
            print(board[2][2].is_attacked_bottom_left(board, 2, 2))
            print(board[2][2].is_protecting_top_right(board, 2, 2))
            print(board[2][2].is_pinned_bottom_left(board, 2, 2))
        print(self.list_of_legal_moves(board))
        self.moves_list = []
