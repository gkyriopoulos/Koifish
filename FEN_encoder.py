def decode_fen(fen):
    fen_parts = fen.split(' ')
    fen_board = fen_parts[0]
    fen_rows = fen_board.split('/')

    board_height = len(fen_rows)
    board_width = max(len(row) for row in fen_rows)

    board = [["**" for _ in range(board_width)] for _ in range(board_height)]

    for row_index, fen_row in enumerate(fen_rows):
        column_index = 0
        for char in fen_row:
            if char.isdigit():
                column_index += int(char)
            else:
                if char.islower():
                    piece = 'b' + char
                else:
                    piece = 'w' + char.lower()
                board[row_index][column_index] = piece
                column_index += 1

    return board


def decode_microchess_fen(fen):
    board = []
    for row in fen.split('/'):
        brow = []
        for c in row:
            if c == ' ':
                break
            elif c in '12345':
                brow.extend(['**'] * int(c))
            elif c == 'p':
                brow.append('bp')
            elif c == 'P':
                brow.append('wp')
            elif c > 'Z':
                brow.append('b' + c)
            else:
                brow.append('w' + c.lower())

        board.append(brow)
    return board


def encode_microchess_fen(board):
    fen = ""

    for row in board:
        fen_row = ""
        empty_count = 0
        for square in row:
            if square == "**":
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                piece = square[1] if square[0] == "b" else square[1].upper()
                fen_row += piece

        if empty_count > 0:
            fen_row += str(empty_count)

        fen += fen_row + "/"

    fen = fen.rstrip("/")  # Remove the trailing '/'

    return fen
