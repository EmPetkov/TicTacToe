from TicTacToeAI import tictactoe


def initiate_board():
    return [['', '', ''], ['', '', ''], ['', '', '']]


class TicTacToePlayer:

    def __init__(self):
        self.board = initiate_board()
        self.winner = False
        print(f"Initialize: {self.board}")

    def play_turn(self, pos: int, player: str = 'X'):
        """ Plays the Player turn """
        coord = self.pos_num_to_coord(pos)
        self.place_on_board(coord=coord, player=player)

    def play_ai_turn(self, player: str = 'O') -> int:
        """ Plays the AI turn """
        ai_pos = tictactoe(self.board)
        coord = self.pos_num_to_coord(ai_pos)
        self.place_on_board(coord=coord, player=player)
        return ai_pos

    @staticmethod
    def pos_num_to_coord(num: int) -> tuple | str:
        """ Converts position number to board coordinates """
        if num < 1 or num > 9:
            return "Invalid input"
        row = (num - 1) // 3
        col = (num - 1) % 3
        return row, col

    def place_on_board(self, coord: tuple, player: str) -> None:
        """ Places the turns in the board """
        self.board[coord[0]][coord[1]] = player
        # self.print_board()
        self.is_winner()
        print(self.is_winner())

    def winner_on_rows(self) -> bool:
        """ Checking if there is winner on rows """
        for i in range(len(self.board)):
            if all(self.board[i][j] == self.board[i][0] and self.board[i][0] != '' for j in range(len(self.board[i]))):
                return True
        return False

    def winner_on_columns(self) -> bool:
        """ Check if there is winner on columns """
        transposed_board = [[self.board[j][i] for j in range(len(self.board))] for i in range(len(self.board[0]))]
        for i in range(len(transposed_board)):
            if all(transposed_board[i][j] == transposed_board[i][0] and transposed_board[i][0] != '' for j in
                   range(len(transposed_board[i]))):
                return True
        return False

    def winner_on_diagonals(self) -> bool:
        """ Check if there is winner in any of the diagonals """
        diag_l = [self.board[i][i] for i in range(len(self.board))]
        diag_r = [self.board[i][len(self.board) - 1 - i] for i in range(len(self.board))]
        diags = [diag_l, diag_r]
        for i in range(len(diags)):
            if all(diags[i][j] == diags[i][0] and diags[i][0] != '' for j in range(len(diags[i]))):
                return True
        return False

    def is_winner(self) -> bool:
        """ Check if there is a winner"""
        if self.winner_on_rows() or self.winner_on_columns() or self.winner_on_diagonals():
            self.winner = True
            return True
        return False

    def is_board_full(self) -> bool:
        """ check if board is already full without a winner """
        for row in self.board:
            if "" in row:
                return False
        return True

    # def print_board(self):
    #     """ Enable in place_on_board for debugging """
    #     for row in self.board:
    #         print(row)
