"""
renderer: all pygame drawing lives here,
kept separate from game logic.
"""

import pygame


# ---------------------------------------------------------
# WINDOW SETTINGS
# ---------------------------------------------------------

WIDTH = 520
HEIGHT = 600

BOARD_SIZE = 360
CELL_SIZE = BOARD_SIZE // 3

# Increased from 100 so that the controls have enough space.
BOARD_TOP = 130

WINDOW_SIZE = (WIDTH, HEIGHT)


# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------

COLOR_BG = (245, 245, 245)
COLOR_LINE = (60, 60, 60)

COLOR_X = (200, 60, 60)
COLOR_O = (60, 100, 200)

COLOR_TEXT = (30, 30, 30)


# ---------------------------------------------------------
# CONVERT MOUSE POSITION TO BOARD CELL
# ---------------------------------------------------------

def board_pos_to_cell(pos):

    x, y = pos

    # Convert screen Y coordinate to board Y coordinate.
    y -= BOARD_TOP

    # Ignore clicks outside the board.
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return None

    col = x // CELL_SIZE
    row = y // CELL_SIZE

    return int(row), int(col)


# ---------------------------------------------------------
# DRAW BOARD
# ---------------------------------------------------------

def draw_board(surface, board):

    surface.fill(COLOR_BG)

    # Draw vertical and horizontal grid lines.
    for i in range(1, 3):

        # Vertical line
        pygame.draw.line(
            surface,
            COLOR_LINE,
            (
                i * CELL_SIZE,
                BOARD_TOP
            ),
            (
                i * CELL_SIZE,
                BOARD_TOP + BOARD_SIZE
            ),
            3
        )

        # Horizontal line
        pygame.draw.line(
            surface,
            COLOR_LINE,
            (
                0,
                BOARD_TOP + i * CELL_SIZE
            ),
            (
                BOARD_SIZE,
                BOARD_TOP + i * CELL_SIZE
            ),
            3
        )

    # Draw X and O.
    for r in range(3):

        for c in range(3):

            symbol = board[r][c]

            if symbol is None:
                continue

            center = (
                c * CELL_SIZE + CELL_SIZE // 2,
                BOARD_TOP
                + r * CELL_SIZE
                + CELL_SIZE // 2
            )

            # Draw X
            if symbol == 'X':

                offset = CELL_SIZE // 3

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (
                        center[0] - offset,
                        center[1] - offset
                    ),
                    (
                        center[0] + offset,
                        center[1] + offset
                    ),
                    6
                )

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (
                        center[0] + offset,
                        center[1] - offset
                    ),
                    (
                        center[0] - offset,
                        center[1] + offset
                    ),
                    6
                )

            # Draw O
            else:

                pygame.draw.circle(
                    surface,
                    COLOR_O,
                    center,
                    CELL_SIZE // 3,
                    6
                )


# ---------------------------------------------------------
# DRAW SCOREBOARD
# ---------------------------------------------------------

def draw_scoreboard(
    surface,
    font,
    x_wins,
    o_wins,
    draws
):

    scoreboard_text = (
        f"X: {x_wins}    "
        f"O: {o_wins}    "
        f"Draws: {draws}"
    )

    draw_text(
        surface,
        font,
        scoreboard_text,
        (10, 5)
    )


# ---------------------------------------------------------
# DRAW TEXT
# ---------------------------------------------------------

def draw_text(
    surface,
    font,
    text,
    pos,
    color=COLOR_TEXT
):

    surface.blit(
        font.render(
            text,
            True,
            color
        ),
        pos
    )


# ---------------------------------------------------------
# DRAW WIN / DRAW BANNER
# ---------------------------------------------------------

def draw_banner(
    surface,
    font,
    text
):

    surf = font.render(
        text,
        True,
        (180, 40, 40)
    )

    # Board ends at:
    #
    # BOARD_TOP + BOARD_SIZE
    #
    # = 130 + 360
    # = 490
    #
    # Place banner around Y = 540 so it is
    # completely visible inside the 600px window.

    rect = surf.get_rect(
        center=(
            surface.get_width() // 2,
            BOARD_TOP + BOARD_SIZE + 50
        )
    )

    surface.blit(
        surf,
        rect
    )