"""
GameEngine: owns the board, turn state, and round-end logic.

You (the player) always play X and click to move.
The computer always plays O and moves automatically right after you,
using a simple random-move AI.
"""

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game.ai import choose_move

HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = HUMAN_SYMBOL
        self.round_over = False
        self.winner = None   # 'X', 'O', or None for a draw

    def handle_click(self, pos):
        # Do not accept moves after the round has ended.
        if self.round_over:
            return

        # Only allow the human player to move when it is X's turn.
        if self.current_player != HUMAN_SYMBOL:
            return

        cell = board_pos_to_cell(pos)

        if cell is None:
            return

        row, col = cell

        # Task 3 will improve this validation.
        # For Task 1, we keep the existing behavior.
        self.board[row][col] = self.current_player

        self.check_round_end()

        # If the round ended, do not switch turns or make another move.
        if self.round_over:
            return

        self.current_player = COMPUTER_SYMBOL
        self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        # Do nothing if the round is already over or it is not
        # the computer's turn.
        if self.round_over or self.current_player != COMPUTER_SYMBOL:
            return

        move = choose_move(self.board)

        if move is None:
            return

        row, col = move
        self.board[row][col] = self.current_player

        self.check_round_end()

        # If the computer's move ended the round, don't switch turns.
        if self.round_over:
            return

        self.current_player = HUMAN_SYMBOL

    def handle_keydown(self, key):
        import pygame

        if key == pygame.K_r:
            self.__init__()

    def check_round_end(self):
        # IMPORTANT:
        # Check for a winner BEFORE checking if the board is full.
        #
        # This ensures that if the final move creates a winning
        # line, it is counted as a win instead of a draw.

        winner = check_winner(self.board)

        if winner:
            self.round_over = True
            self.winner = winner
            return

        # Only check for draw if there is no winner.
        if is_board_full(self.board):
            self.round_over = True
            self.winner = None
            return

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_board(surface, self.board)

        turn_label = (
            "Your turn (X)"
            if self.current_player == HUMAN_SYMBOL
            else "Computer's turn (O)"
        )

        renderer.draw_text(
            surface,
            font,
            turn_label,
            (10, 20)
        )

        if self.round_over:
            text = (
                f"{self.winner} wins!"
                if self.winner
                else "Draw!"
            )

            renderer.draw_banner(
                surface,
                font,
                f"{text} Press R for a new round."
            )