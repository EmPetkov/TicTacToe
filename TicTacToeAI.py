import random


def tictactoe(board):
    # Create a list of all possible winning combinations
    winning_combinations = [
        [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],  # Rows
        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],  # Columns
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]  # Diagonals
    ]

    # Check for possible wins for O and finish them
    for combination in winning_combinations:
        positions = [board[row][col] for row, col in combination]
        if positions.count("O") == 2 and positions.count("") == 1:
            index = positions.index("")
            return combination[index][0] * 3 + combination[index][1] + 1

    # Check for possible wins for X and block them
    for combination in winning_combinations:
        positions = [board[row][col] for row, col in combination]
        if positions.count("X") == 2 and positions.count("") == 1:
            index = positions.index("")
            return combination[index][0] * 3 + combination[index][1] + 1

    # Try to fill a row, column or diagonal
    for combination in winning_combinations:
        positions = [board[row][col] for row, col in combination]
        if positions.count("O") == 1 and positions.count("") == 2:
            index = positions.index("")
            return combination[index][0] * 3 + combination[index][1] + 1

    # Place random free space
    free_spaces = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ""]
    if free_spaces:
        row, col = random.choice(free_spaces)
        return row * 3 + col + 1

    # If there are no free spaces, return None (game over)
    return None
