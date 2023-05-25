import pygame
import pygame.display
import pygame.draw_py

import Engine

normalBoard = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["**", "**", "**", "**", "**", "**", "**", "**"],
    ["**", "**", "**", "**", "**", "**", "**", "**"],
    ["**", "**", "**", "**", "**", "**", "**", "**"],
    ["**", "**", "**", "**", "**", "**", "**", "**"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]

boardLosAlamos = [
    ["br", "bn", "bq", "bk", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp"],
    ["**", "**", "**", "**", "**", "**"],
    ["**", "**", "**", "**", "**", "**"],
    ["wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wq", "wk", "wn", "wr"]]

boardMicroChess = [
    ["bk", "bn", "bb", "br"],
    ["bp", "**", "**", "**"],
    ["**", "**", "**", "**"],
    ["**", "**", "**", "wp"],
    ["wr", "wb", "wn", "wk"]]

pieces = ["br", "bn", "bb", "bq", "bk", "bp", "wr", "wn", "wb", "wq", "wk", "wp"]

img = {}

color_white = [240, 217, 181, 255]
color_black = [181, 136, 99, 255]

colors = [pygame.Color(color_white), pygame.Color(color_black)]

# Function that loads piece images from the disk.
def load_assets(piece_width, piece_height):
    for piece in pieces:
        img[piece] = pygame.transform.scale(pygame.image.load("misc/" + piece + ".png"), (piece_width, piece_height))


# Function that draws a board:
def draw_board(screen, board, dim_x, dim_y, square_width, square_height):
    for i in range(dim_x):
        for j in range(dim_y):
            color_index = (i + j) % 2
            pygame.draw.rect(screen, colors[color_index], pygame.Rect(i * square_width, j * square_height, square_width, square_height))

    for i in range(dim_x):
        for j in range(dim_y):
            piece = board[j][i]
            if piece != "**":
                screen.blit(img[piece], pygame.Rect(i * square_width, j * square_height, square_width, square_height))

def main():

    #Choices are boardNormal,boardLosAlamos,boardMicroChess
    board = boardMicroChess

    # Assigning the aspect ratio for each board.
    if board == boardMicroChess:
        window_width = 256
        window_height = 320
        dim_x = 4
        dim_y = 5
    elif board == boardLosAlamos:
        window_width = 384
        window_height = 384
        dim_x = 6
        dim_y = 6
    else:
        board = normalBoard
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

    print("Hello world!")

    # Opening the window.
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        # Draw current board.
        draw_board(screen, board, dim_x, dim_y, square_width, square_height)
        pygame.display.flip()


if __name__ == "__main__":
    main()
