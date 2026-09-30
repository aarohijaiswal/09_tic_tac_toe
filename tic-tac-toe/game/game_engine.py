"""
GameEngine: owns the board, turn state, round-end logic, and scoreboard.

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
        self.winner = None

        # Task 2: Persistent scoreboard
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

    def reset_round(self):
        """
        Reset only the current round.

        The scoreboard is NOT reset.
        """
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = HUMAN_SYMBOL
        self.round_over = False
        self.winner = None

    def reset_match(self):
        """
        Reset the entire match.

        This resets both the current round and the scoreboard.
        Task 4 will later provide a separate control for this.
        """
        self.reset_round()

        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

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

        # Task 3 will add occupied-cell validation.
        self.board[row][col] = self.current_player

        self.check_round_end()

        # If the round ended, do not switch turns or make
        # the computer move.
        if self.round_over:
            return

        self.current_player = COMPUTER_SYMBOL
        self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        if self.round_over or self.current_player != COMPUTER_SYMBOL:
            return

        move = choose_move(self.board)

        if move is None:
            return

        row, col = move
        self.board[row][col] = self.current_player

        self.check_round_end()

        # If the computer's move ended the round,
        # don't switch turns.
        if self.round_over:
            return

        self.current_player = HUMAN_SYMBOL

    def handle_keydown(self, key):
        import pygame

        # R = restart current round
        # Scoreboard remains unchanged.
        if key == pygame.K_r:
            self.reset_round()

    def check_round_end(self):
        # IMPORTANT:
        # Check winner BEFORE checking whether the board is full.
        winner = check_winner(self.board)

        if winner:
            self.round_over = True
            self.winner = winner

            # Update the appropriate score exactly once.
            if winner == HUMAN_SYMBOL:
                self.x_wins += 1
            elif winner == COMPUTER_SYMBOL:
                self.o_wins += 1

            return

        # Only check for draw if there is no winner.
        if is_board_full(self.board):
            self.round_over = True
            self.winner = None

            # Update draw count.
            self.draws += 1

            return

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_board(surface, self.board)

        # Display scoreboard.
        renderer.draw_scoreboard(
            surface,
            font,
            self.x_wins,
            self.o_wins,
            self.draws
        )

        # Display current turn.
        turn_label = (
            "Your turn (X)"
            if self.current_player == HUMAN_SYMBOL
            else "Computer's turn (O)"
        )

        renderer.draw_text(
            surface,
            font,
            turn_label,
            (10, 50)
        )

        # Display result when round is over.
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