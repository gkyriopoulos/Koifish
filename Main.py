import pygame
import pygame.display
import pygame.draw_py
import Engine

pieces = ["br", "bn", "bb", "bq", "bk", "bp", "wr", "wn", "wb", "wq", "wk", "wp"]

img = {}

# Colors for the chessboard
colors = [pygame.Color([240, 217, 181, 255]), pygame.Color([181, 136, 99, 255])]


# Function that loads piece images from the disk.
def load_assets(piece_width, piece_height):
    for piece in pieces:
        img[piece] = pygame.transform.scale(pygame.image.load("misc/" + piece + ".png"), (piece_width, piece_height))


# Function that draws a board:
def draw_board(screen, board, dim_x, dim_y, square_width, square_height):
    for i in range(dim_x):
        for j in range(dim_y):
            # Coloring the board
            color_index = (i + j) % 2
            pygame.draw.rect(screen, colors[color_index],
                             pygame.Rect(i * square_width, j * square_height, square_width, square_height))
            piece = board[j][i]
            if piece != "**":
                screen.blit(img[piece], pygame.Rect(i * square_width, j * square_height, square_width, square_height))


def main():
    # Choices are Normal, LosAlamos, MicroChess
    board_choice = "MicroChess"

    # Assigning the aspect ratio for each board.
    if board_choice == "MicroChess":
        window_width = 256
        window_height = 320
        dim_x = 4
        dim_y = 5
    elif board_choice == "LosAlamos":
        window_width = 384
        window_height = 384
        dim_x = 6
        dim_y = 6
    else:
        board_choice = "Normal"
        window_width = 512
        window_height = 512
        dim_x = 8
        dim_y = 8

    # Making piece's size proportional to the screen size.
    square_width = window_width // dim_x
    square_height = window_height // dim_y

    # Loading piece's images from the disk.
    load_assets(square_width, square_height)

    # Initialising the screen.
    screen = pygame.display.set_mode((window_width, window_height))

    my_engine = Engine.Engine(board_choice)
    board = my_engine.board

    src = []
    dst = []
    total_clicks = 0
    player = "w"
    # Opening the window.
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                cords = pygame.mouse.get_pos()
                cords_x = cords[0] // square_width
                cords_y = cords[1] // square_height
                # if (we choose the same coord reset or (if it's not dst click, and we choose empty tile) )
                # => reset dst, src
                if src == [cords_y, cords_x] or (my_engine.board[cords_y][cords_x] == "**" and total_clicks == 0):
                    dst.clear()
                    src.clear()
                    total_clicks = 0
                elif total_clicks == 0:
                    src = [cords_y, cords_x]
                    total_clicks += 1
                elif total_clicks == 1:
                    dst = [cords_y, cords_x]
                    board = my_engine.attempt_move((src[0], src[1]), (dst[0], dst[1]), player)
                    if my_engine.board_has_changed:
                        # After making a move swap player.
                        player = "b" if player == "w" else "w"
                    dst.clear()
                    src.clear()
                    total_clicks = 0

        # Draw current board.
        draw_board(screen, board, dim_x, dim_y, square_width, square_height)
        pygame.display.update()
        # Testing type moves
        # type_src = input("Src: ")
        # type_dst = input("Dst: ")
        # my_engine.type_move(type_src, type_dst)


if __name__ == "__main__":
    main()
