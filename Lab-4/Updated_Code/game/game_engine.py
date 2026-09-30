"""
GameEngine: owns the board, turn state, round-end logic,
scoreboard, first-player selection, and reset controls.

Human player always plays X.
Computer always plays O.
"""

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game.ai import choose_move


HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        # 3x3 game board
        self.board = [[None] * 3 for _ in range(3)]

        # Player who starts the round
        self.starting_player = HUMAN_SYMBOL

        # Current player
        self.current_player = self.starting_player

        # Round state
        self.round_over = False
        self.winner = None

        # Persistent scoreboard
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

    # ---------------------------------------------------------
    # ROUND / MATCH RESET
    # ---------------------------------------------------------

    def reset_round(self):
        """
        Restart only the current round.

        The scoreboard is preserved.
        The selected starting player is preserved.
        """

        self.board = [[None] * 3 for _ in range(3)]

        self.current_player = self.starting_player

        self.round_over = False
        self.winner = None

        # If O is selected as the starter,
        # the computer must automatically make the first move.
        self._maybe_take_computer_turn()

    def reset_match(self):
        """
        Reset the entire match.

        This clears the scoreboard and starts a fresh round.
        """

        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        self.reset_round()

    # ---------------------------------------------------------
    # STARTING PLAYER
    # ---------------------------------------------------------

    def set_starting_player(self, player):
        """
        Set X or O as the starting player.

        Selecting X or O starts a new round using that player.
        """

        if player not in (HUMAN_SYMBOL, COMPUTER_SYMBOL):
            return

        self.starting_player = player

        # Start a new round with the selected player.
        self.reset_round()

    # ---------------------------------------------------------
    # HUMAN PLAYER MOVE
    # ---------------------------------------------------------

    def handle_click(self, pos):

        # Do not accept moves after the round has ended.
        if self.round_over:
            return

        # Only allow X/human to make a mouse move.
        if self.current_player != HUMAN_SYMBOL:
            return

        cell = board_pos_to_cell(pos)

        # Click was outside the board.
        if cell is None:
            return

        row, col = cell

        # -----------------------------------------------------
        # TASK 3:
        # Do not allow an occupied cell to be overwritten.
        # -----------------------------------------------------

        if self.board[row][col] is not None:
            return

        # Place X.
        self.board[row][col] = HUMAN_SYMBOL

        # Check whether this move ended the round.
        self.check_round_end()

        # If the round ended, stop here.
        if self.round_over:
            return

        # Switch to computer.
        self.current_player = COMPUTER_SYMBOL

        # Computer makes its move.
        self._maybe_take_computer_turn()

    # ---------------------------------------------------------
    # COMPUTER MOVE
    # ---------------------------------------------------------

    def _maybe_take_computer_turn(self):

        # Do nothing if round is already over.
        if self.round_over:
            return

        # Do nothing if it is not O's turn.
        if self.current_player != COMPUTER_SYMBOL:
            return

        move = choose_move(self.board)

        if move is None:
            return

        row, col = move

        # Place O.
        self.board[row][col] = COMPUTER_SYMBOL

        # Check whether computer's move ended the round.
        self.check_round_end()

        # If the round ended, don't switch turns.
        if self.round_over:
            return

        # Give control back to human.
        self.current_player = HUMAN_SYMBOL

    # ---------------------------------------------------------
    # KEYBOARD CONTROLS
    # ---------------------------------------------------------

    def handle_keydown(self, key):
        import pygame

        # X = X starts the next round
        if key == pygame.K_x:
            self.set_starting_player(HUMAN_SYMBOL)

        # O = O starts the next round
        elif key == pygame.K_o:
            self.set_starting_player(COMPUTER_SYMBOL)

        # R = Restart current round
        # Scoreboard is preserved.
        elif key == pygame.K_r:
            self.reset_round()

        # M = Reset entire match
        # Scoreboard becomes zero.
        elif key == pygame.K_m:
            self.reset_match()

    # ---------------------------------------------------------
    # WIN / DRAW DETECTION
    # ---------------------------------------------------------

    def check_round_end(self):

        # IMPORTANT:
        # Check for a winner BEFORE checking whether the
        # board is full.
        #
        # This ensures that a winning final move is counted
        # as a WIN instead of a DRAW.

        winner = check_winner(self.board)

        if winner:

            self.round_over = True
            self.winner = winner

            # Update scoreboard exactly once.
            if winner == HUMAN_SYMBOL:
                self.x_wins += 1

            elif winner == COMPUTER_SYMBOL:
                self.o_wins += 1

            return

        # Only declare a draw if there is no winner.
        if is_board_full(self.board):

            self.round_over = True
            self.winner = None

            self.draws += 1

            return

    # ---------------------------------------------------------
    # DRAW EVERYTHING
    # ---------------------------------------------------------

    def draw(self, surface, font):
        from game import renderer

        # Draw board and X/O symbols.
        renderer.draw_board(
            surface,
            self.board
        )

        # Draw scoreboard.
        renderer.draw_scoreboard(
            surface,
            font,
            self.x_wins,
            self.o_wins,
            self.draws
        )

        # Display current turn.
        if self.round_over:

            turn_label = "Round over"

        elif self.current_player == HUMAN_SYMBOL:

            turn_label = "Your turn (X)"

        else:

            turn_label = "Computer's turn (O)"

        renderer.draw_text(
            surface,
            font,
            turn_label,
            (10, 50)
        )

        # -----------------------------------------------------
        # CONTROLS
        # -----------------------------------------------------

        renderer.draw_text(
            surface,
            font,
            "X: Start X     O: Start O",
            (10, 75)
        )

        renderer.draw_text(
            surface,
            font,
            "R: Restart Round     M: Reset Match",
            (10, 100)
        )

        # -----------------------------------------------------
        # ROUND RESULT
        # -----------------------------------------------------

        if self.round_over:

            if self.winner:
                text = f"{self.winner} wins!"
            else:
                text = "Draw!"

            renderer.draw_banner(
                surface,
                font,
                f"{text} Press R for a new round."
            )