import pygame
import pygame.display
import pygame.draw_py
import Engine

pygame.init()

pieces = ["br", "bn", "bb", "bq", "bk", "bp", "wr", "wn", "wb", "wq", "wk", "wp"]

img = {}

img_x = 60
img_y = 60

# Colors for the chessboard
colors = [pygame.Color([240, 217, 181, 255]), pygame.Color([181, 136, 99, 255])]
highlight_colors = pygame.Color([164, 212, 129, 255])
bg_colors = pygame.Color([49, 46, 43, 255])
button_colors = [pygame.Color([65, 62, 57, 255]), pygame.Color([56, 53, 49, 255])]


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
        pygame.draw.circle(screen, highlight_colors
                           , (square_width * square[1][1] + square_width / 2
                              , square_height * square[1][0] + square_height / 2)
                           , 10)


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


def main():
    # Choices are Normal, LosAlamos, MicroChess
    board_choice = "Normal"

    # Assigning the aspect ratio for each board.
    if board_choice == "MicroChess":
        dim_x = 4
        dim_y = 5
        # window_width = 2 * dim_x * img_x
        window_width = dim_x * img_x
        window_height = dim_y * img_y
    elif board_choice == "LosAlamos":
        dim_x = 6
        dim_y = 6
        # window_width = 2 * dim_x * img_x
        window_width = dim_x * img_x
        window_height = dim_y * img_y
    else:
        board_choice = "Normal"
        dim_x = 8
        dim_y = 8
        # window_width = 2 * dim_x * img_x
        window_width = dim_x * img_x
        window_height = dim_y * img_y

    # Making piece's size proportional to the screen size.
    square_width = window_width // dim_x
    square_height = window_height // dim_y

    # Loading piece's images from the disk.
    # load_assets(square_width / 2, square_height)
    load_assets(square_width, square_height)

    # Initialising the screen.
    screen = pygame.display.set_mode((window_width, window_height))
    screen.fill(bg_colors)

    my_engine = Engine.Engine(board_choice)

    board = my_engine.board

    src = []
    dst = []
    highlighted_moves = []
    threatmap = []
    threatmap_clicks = 0
    pinray = []
    pinray_clicks = 0
    total_clicks = 0
    player = "w"

    # Button stuff
    # button_len = (220, 35)
    # button_center = (window_width / 2 + window_width / 4, window_height/10)
    # button_pos = (button_center[0] - button_len[0] / 2, button_center[1] - button_len[1] / 2)

    # Opening the window.
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                # Check that the click is inside the chess board.
                # coords_x = 2 * coords[0] // square_width
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
                        board = my_engine.attempt_move((src[0], src[1]), (dst[0], dst[1]), player)

                        if board == "b":
                            break
                        elif board == "w":
                            break
                        elif board == "d":
                            break

                        if my_engine.board_has_changed:
                            # After making a move swap player.
                            player = "b" if player == "w" else "w"

                        dst.clear()
                        src.clear()
                        total_clicks = 0

                # Button stuff
                # if button_pos[0] <= coords[0] <= button_pos[0] + button_len[0] and button_pos[1] <= coords[1] <= \
                #         button_pos[1] + button_len[1]:
                #     if threat_map_clicks == 0:
                #         threat_map = my_engine.threatmap
                #         threat_map_clicks += 1
                #     else:
                #         threat_map = []
                #         threat_map_clicks = 0

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

        # Button stuff
        # x, y = pygame.mouse.get_pos()
        # if button_pos[0] <= x <= button_pos[0] + button_len[0] and button_pos[1] <= y <= button_pos[1] + button_len[1]:
        #     draw_threatmap_button(screen, button_colors[0], button_len, button_center, button_pos)
        # else:
        #     draw_threatmap_button(screen, button_colors[1], button_len, button_center, button_pos)
        # draw_board(screen, board, dim_x, dim_y, square_width / 2, square_height)

        # If the game is not over draw the board.
        if board == "b":
            print("Black Wins!")
            running = False
        elif board == "w":
            print("White Wins!")
            running = False
        elif board == "d":
            print("Draw!")
            running = False
        else:
            draw_board(screen, board, dim_x, dim_y, square_width, square_height)

        if highlighted_moves:
            draw_highlights(screen, square_width, square_height, highlighted_moves)

        if threatmap:
            draw_threatmap(screen, square_width, square_height, threatmap)

        if pinray:
            draw_pinray(screen, square_width, square_height, pinray)

        # if highlighted_moves:
        # draw_highlights(screen, square_width / 2, square_height, highlighted_moves)
        # if threat_map:
        #     draw_threatmap(screen, square_width / 2, square_height, threat_map)
        # if pinray:
        #     draw_threatmap(screen, square_width / 2, square_height, pinray)

        pygame.display.update()


if __name__ == "__main__":
    main()
