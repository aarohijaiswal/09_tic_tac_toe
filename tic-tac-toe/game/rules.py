"""
rules: win/draw detection for a 3x3 board.

board is a 3x3 list of lists, each cell is None, 'X', or 'O'.
"""


def check_winner(board):
    # All 8 possible winning lines:
    # 3 rows + 3 columns + 2 diagonals
    lines = [
        # Rows
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],

        # Columns
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],

        # Diagonals
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]

    for line in lines:
        if line[0] is not None and line[0] == line[1] == line[2]:
            return line[0]

    return None


def is_board_full(board):
    return all(cell is not None for row in board for cell in row)