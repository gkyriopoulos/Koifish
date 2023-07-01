#!/usr/bin/env python3
import pygame
import pygame.display
import pygame.draw_py
import Agent
import Engine
import Trainer
import Utils

pygame.init()

pieces = ["br", "bn", "bb", "bq", "bk", "bp", "wr", "wn", "wb", "wq", "wk", "wp"]
img = {}
img_x = 60
img_y = 60

# Colors for the chessboard
colors = [pygame.Color([240, 217, 181, 255]), pygame.Color([181, 136, 99, 255])]
highlight_colors = pygame.Color([164, 212, 129, 255])
bg_colors = pygame.Color([49, 46, 43, 255])


def main():
    eye_candy()
    # Choices are Normal, LosAlamos, MicroChess
    player = "b"
    agent_player = "w"
    board_choice = "RKvsRK"
    mode = "pve"

    train_agent = True
    # , "KvsPK", "PKvsK", "RNKvsRK", "RKvsRNK"
    training_boards = ["RKvsRK"]
    print_graphs = False
    save_stats = True
    train_white = True
    train_black = True

    episodes = 5000000

    if train_agent:
        for b in training_boards:
            Trainer.train(b, episodes, print_graphs, save_stats, train_white, train_black)

    if mode == "pve":
        # Creating an agent to play against.
        my_agent = Agent.QLearningAgent(board_choice, agent_player)

    # Assigning the aspect ratio for each board.
    if board_choice == "MicroChess" or "RKvsRK" or "PKvsK" or "KvsPK" or "RNKvsRK" or "RKvsRNK":
        dim_x = 4
        dim_y = 5
        window_width = dim_x * img_x
        window_height = dim_y * img_y
    elif board_choice == "LosAlamos":
        dim_x = 6
        dim_y = 6
        window_width = dim_x * img_x
        window_height = dim_y * img_y
    else:
        board_choice = "Normal"
        dim_x = 8
        dim_y = 8
        window_width = dim_x * img_x
        window_height = dim_y * img_y

    # Making piece's size proportional to the screen size.
    square_width = window_width // dim_x
    square_height = window_height // dim_y

    # Loading piece's images from the disk.
    load_assets(square_width, square_height)

    # Initialising the screen.
    screen = pygame.display.set_mode((window_width, window_height))
    screen.fill(bg_colors)

    src = []
    dst = []
    highlighted_moves = []
    threatmap = []
    threatmap_clicks = 0
    pinray = []
    pinray_clicks = 0
    total_clicks = 0

    # Opening the window.
    play_again = True
    while play_again:
        running = True
        my_engine = Engine.Engine(board_choice)
        board = my_engine.board
        draw_board(screen, board, dim_x, dim_y, square_width, square_height)
        pygame.display.update()
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    coords = pygame.mouse.get_pos()
                    # Check that the click is inside the chess board.
                    coords_x = coords[0] // square_width
                    coords_y = coords[1] // square_height
                    if 0 <= coords_x < dim_x and 0 <= coords_y < dim_y:
                        highlighted_moves = []
                        # if (we choose the same coord reset or (if it's not dst click, and we choose empty tile) )
                        # => reset dst, src
                        if src == [coords_y, coords_x] or (
                                my_engine.board[coords_y][coords_x] == "**" and total_clicks == 0):
                            dst.clear()
                            src.clear()
                            total_clicks = 0
                        elif total_clicks == 0:
                            src = [coords_y, coords_x]
                            total_clicks += 1
                            legal_moves = my_engine.legal_moves
                            selected_moves = my_engine.get_pieces_moves(src, my_engine.get_piece(src), player)
                            highlighted_moves = set(legal_moves).intersection(selected_moves)
                            # Castling highlights gui stuff
                            if ((7, 4), (7, 7)) in legal_moves and src == [7, 4]:
                                highlighted_moves.add(((7, 4), (7, 5)))
                                highlighted_moves.add(((7, 4), (7, 6)))
                                highlighted_moves.add(((7, 4), (7, 7)))
                            if ((0, 4), (0, 7)) in legal_moves and src == [0, 4]:
                                highlighted_moves.add(((0, 4), (0, 5)))
                                highlighted_moves.add(((0, 4), (0, 6)))
                                highlighted_moves.add(((0, 4), (0, 7)))
                            if ((7, 4), (7, 0)) in legal_moves and src == [7, 4]:
                                highlighted_moves.add(((7, 4), (7, 3)))
                                highlighted_moves.add(((7, 4), (7, 2)))
                                highlighted_moves.add(((7, 4), (7, 1)))
                                highlighted_moves.add(((7, 4), (7, 0)))
                            if ((0, 4), (0, 0)) in legal_moves and src == [0, 4]:
                                highlighted_moves.add(((0, 4), (0, 3)))
                                highlighted_moves.add(((0, 4), (0, 2)))
                                highlighted_moves.add(((0, 4), (0, 1)))
                                highlighted_moves.add(((0, 4), (0, 0)))
                        elif total_clicks == 1:
                            # Added because of a threatmap bug
                            if threatmap_clicks == 1:
                                threatmap = []
                                threatmap_clicks = 0
                            if pinray_clicks == 1:
                                pinray = []
                                pinray_clicks = 0

                            dst = [coords_y, coords_x]
                            board = my_engine.attempt_move((src[0], src[1]), (dst[0], dst[1]), player)[0]
                            # print(my_engine.score)

                            if my_engine.winner == "b":
                                break
                            elif my_engine.winner == "w":
                                break
                            elif my_engine.winner == "d":
                                break

                            if mode == "pvp":
                                if my_engine.board_has_changed:
                                    # After making a move swap player.
                                    player = "b" if player == "w" else "w"

                            dst.clear()
                            src.clear()
                            total_clicks = 0

                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_t:
                        if threatmap_clicks == 0:
                            threatmap = my_engine.threatmap
                            threatmap_clicks += 1
                        else:
                            threatmap = []
                            threatmap_clicks = 0
                    if e.key == pygame.K_p:
                        if pinray_clicks == 0:
                            pinray = my_engine.pinrays
                            pinray_clicks += 1
                        else:
                            pinray = []
                            pinray_clicks = 0

            if my_engine.turn_player == agent_player and mode == "pve" and my_engine.winner == "None":
                # If agent is white wait a bit before making the first move.
                if my_engine.moves == 0 and agent_player == "w":
                    pygame.time.wait(600)
                encoded_board = Utils.encode_microchess_fen(my_engine.board)
                my_agent.actions = my_engine.legal_moves
                action = my_agent.choose_action(encoded_board)
                board = my_engine.attempt_move(action[0], action[1], agent_player)[0]

            # If the game is not over draw the board.
            if my_engine.winner == "b":
                print("Black Wins!")
                running = False
            elif my_engine.winner == "w":
                print("White Wins!")
                running = False
            elif my_engine.winner == "d":
                print("Draw!")
                running = False

            draw_board(screen, board, dim_x, dim_y, square_width, square_height)

            if highlighted_moves:
                draw_highlights(screen, square_width, square_height, highlighted_moves)

            if threatmap:
                draw_threatmap(screen, square_width, square_height, threatmap)

            if pinray:
                draw_pinray(screen, square_width, square_height, pinray)

            pygame.display.update()

        user_input = input("Do you want to play again? (y/n)")
        if user_input == "y":
            play_again = True
            if mode == "pvp":
                if player == "b":
                    player = "w"
        else:
            play_again = False


# Function that loads piece images from the disk.
def load_assets(piece_width, piece_height):
    for piece in pieces:
        img[piece] = pygame.transform.scale(pygame.image.load("misc/" + piece + ".png"), (piece_width, piece_height))


# Function that draws a board:
def draw_board(screen, board, dim_x, dim_y, square_width, square_height):
    for i in range(dim_x):
        for j in range(dim_y):
            color_index = (i + j) % 2
            pygame.draw.rect(screen, colors[color_index],
                             pygame.Rect(i * square_width, j * square_height, square_width, square_height))
            piece = board[j][i]
            if piece != "**":
                screen.blit(img[piece], pygame.Rect(i * square_width, j * square_height, square_width, square_height))


def draw_highlights(screen, square_width, square_height, squares):
    for square in squares:
        pygame.draw.circle(screen, highlight_colors, (square_width * square[1][1] + square_width / 2,
                                                      square_height * square[1][0] + square_height / 2), 10)


def draw_threatmap(screen, square_width, square_height, squares):
    for square in squares:
        font = pygame.font.SysFont('Sans-serif', int(50), bold=False)
        surf = font.render('X', True, 'Red')
        surf_rect = surf.get_rect(center=(square_width * square[1] + (square_width / 2),
                                          square_height * square[0] + (square_height / 2)))
        screen.blit(surf, surf_rect)


def draw_threatmap_button(screen, color, length, center, pos):
    font = pygame.font.SysFont('Sans-serif', int(30), bold=False)
    surf = font.render('Show Threatmap', True, 'white')
    surf_rect = surf.get_rect(center=(center[0], center[1]))
    button = pygame.Rect(pos[0], pos[1], length[0], length[1])
    pygame.draw.rect(screen, color, button)
    screen.blit(surf, surf_rect)


def draw_pinray(screen, square_width, square_height, squares):
    for square in squares:
        font = pygame.font.SysFont('Sans-serif', int(50), bold=False)
        surf = font.render('X', True, 'Blue')
        surf_rect = surf.get_rect(center=(square_width * square[1] + (square_width / 2),
                                          square_height * square[0] + (square_height / 2)))
        screen.blit(surf, surf_rect)


def eye_candy():
    koi_fish = r'''
####################################
        Welcome to Koifish!         
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡅⠀⣸⣿⣿⣿⠿⠟⠛⠿⣿⠆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⠟⠁⣠⣶⣶⣦⣤⣤⣾⣷⣄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠉⣁⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⣀⠀⠀⠀⣴⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀
⢠⣤⣄⡀⣼⣿⣧⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀
⠘⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀
⠀⠈⠻⢿⣿⣿⣿⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠿⠿⠿⠿⠟⠛⠛⠉⠀
⠀⠀⠀⠀⠀    
Copyright 
© 2023 Joel Jani &
George Kyriopoulos           
###################################
    '''
    print(koi_fish)
    pygame.time.wait(500)


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', "output.dat")
    #
    # import pstats
    # from pstats import SortKey
    #
    # p = pstats.Stats("output.dat")
    # p.sort_stats()
    # p.dump_stats("results.prof")
    main()
