import pygame

class Board:
    board = []
    
    def edit_board(self, edited_board):
        if type(edited_board) == list:
            self.board = edited_board
    
    def set_start_position(self, pieces):
        #pieces list:         [wr, wn, wb, wq, wk, wp, bp, br, bn, bb, bq, bk]
        self.board.append([pieces[7], pieces[8], pieces[9], pieces[10], pieces[11], pieces[9], pieces[8], pieces[7]])
        self.board.append([pieces[6]] * 8)

        for i in range(4):
            self.board.append([0] * 8)

        self.board.append([pieces[5]] * 8)
        self.board.append([pieces[0], pieces[1], pieces[2], pieces[3], pieces[4], pieces[2], pieces[1], pieces[0]])