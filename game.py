class Game:
    king_positions = [[7, 4], [0, 4]]
    last_move = [0, 0]
    team_on_move = 0
    opposite_team = 1

    def square_is_attacked(self, board, row, col, team):
        attacked = False
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0 and board[i][j].team == team and [row, col] in board[i][j].possible_moves_list(board, i, j):
                        attacked = True
                        break
        return attacked

    def make_move_if_legal(self, testing_board, first_board, startRow, startCol, endRow, endCol):
        legality = True
        if testing_board[startRow][startCol].team == self.team_on_move and [endRow, endCol] in testing_board[startRow][startCol].possible_moves_list(testing_board, startRow, startCol):
            #en pessant
            if testing_board[startRow][startCol].value == 1 and startRow != endRow and startCol != endCol and testing_board[endRow][endCol] == 0:
                if self.last_move == [startRow, endCol] and testing_board[startRow][endCol].value == 1:
                    testing_board[endRow][endCol] = testing_board[startRow][startCol]
                    testing_board[startRow][startCol] = testing_board[startRow][endCol] = 0
            #castling
            elif testing_board[startRow][startCol].value == 0 and startRow == endRow and endCol in [startCol + 2, startCol - 2]:
                #first we need to check if king is in check - in this case castling is not possible
                if self.square_is_attacked(testing_board, startRow, startCol):
                    legality = False
                #short castle
                if endCol > startCol:
                    if self.square_is_attacked(testing_board, startRow, startCol + 1) or self.square_is_attacked(testing_board, startRow, startCol + 2):
                        legality = False
                #long castle
                else:
                    if self.square_is_attacked(testing_board, startRow, startCol - 1) or self.square_is_attacked(testing_board, startRow, startCol - 2):
                        legality = False
                testing_board[endRow][endCol] = testing_board[startRow][startCol]
                if endCol > startCol:
                    testing_board[startRow][startCol + 1] = testing_board[startRow][7]
                    testing_board[startRow][7] = 0
                else:
                    testing_board[startRow][startCol - 1] = testing_board[startRow][0]
                    testing_board[startRow][0] = 0
            else:
                testing_board[endRow][endCol] = testing_board[startRow][startCol]
                testing_board[startRow][startCol] = 0
            if not self.square_is_attacked(testing_board, *self.king_positions[self.team_on_move], self.opposite_team) and legality:
                self.last_move = [endRow, endCol]
                if testing_board[endRow][endCol] != 0 and testing_board[endRow][endCol].value == 0:
                    self.king_positions[self.team_on_move] = [endRow, endCol]
                if self.team_on_move == 0:
                    self.team_on_move = 1
                    self.opposite_team = 0
                else:
                    self.team_on_move = 0
                    self.opposite_team = 1
                    print('gituwa')
                first_board = testing_board
            else:
                testing_board = first_board
