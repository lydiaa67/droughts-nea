import pygame
import sys
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, RED, COLS, ROWS, piece_sound
from checkers.game import Game
from minimax.algorithm import minimax
from checkers.board import Board

timer_height = 70
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # win means window
pygame.display.set_caption('Checkers')

FPS = 60  # not in constants folder as it is not specific to the game, rather the display

def get_row_col_from_mouse(pos):
    x, y = pos
    # row = y // SQUARE_SIZE
    # col = x // SQUARE_SIZE
    offset_x = (800 - (SQUARE_SIZE * COLS)) // 2  # Centering offset
    x_adjusted = x - offset_x  # Shift x-coordinate back to board's actual position

    # Only process clicks inside the board area
    if not (0 <= x_adjusted < SQUARE_SIZE * COLS and 70 <= y < 70 + (SQUARE_SIZE * ROWS)):
        return None  # This prevents crashes when clicking outside

    row = (y - 70) // SQUARE_SIZE  # Adjust for timer space
    col = x_adjusted // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    total_nodes = 0  # Initialises total_nodes
    turn_start_time = pygame.time.get_ticks()
    
    d_count = 0
    global depth
    from menu import difficulty
    if difficulty == "easy":
        depth = 3
    elif difficulty == "medium":
        depth = 4
    else:
        depth = 5

    while run and (((pygame.time.get_ticks() - turn_start_time)/1000) < game.BLACK_time):
        clock.tick(FPS)

        game.board.dynamic_depth(d_count, depth)

        if game.turn == RED:
            # Run minimax with alpha-beta pruning and node counting
            value, new_board, nodes_evaluated = minimax(game.get_board(), depth, True, game)
            total_nodes += nodes_evaluated  # Add the nodes from this turn
            game.ai_move(new_board)
            piece_sound.play()

        winner = game.winner()  # Store winner once

        if winner:  # If a winner is found
            print(winner)
            pygame.time.delay(2000)  # Small delay for transition effect
            run = False
            break  # Exit loop immediately to avoid extra checks

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_b):
                run = False

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row_col = get_row_col_from_mouse(pos)

                if row_col is not None:
                    row, col = row_col
                    game.select(row, col)

            game.update()

    # Store winner once before exiting the loop
    winner = game.winner()  

    seconds = (pygame.time.get_ticks() - turn_start_time) / 1000
    print(f"You took: {seconds} seconds to win/lose")
    print(f"Total nodes evaluated by AI: {total_nodes}")

    # Transition to the correct screen after the game loop exits
    if winner == "RED wins!" or seconds >= game.BLACK_time: 
        from menu import loser
        loser()
    elif winner == "BLACK wins!":
        from menu import winner
        winner()

from menu import main_menu
main_menu()