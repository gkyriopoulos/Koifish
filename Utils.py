import ijson
import ujson
import os


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


# def save_q(agent):
#     converted_data = {}
#     converted_data = {str(key): value for key, value in agent.q_values.items()}
#
#     with open(agent.file_name, "w") as file:
#         ujson.dump(converted_data, file)

def save_q(agent):
    converted_data = {}
    converted_data = {str(key): value for key, value in agent.q_values.items()}

    # Use dumps to convert the data into a JSON string
    json_string = ujson.dumps(converted_data)

    with open(agent.file_name, "w") as file:
        # Write the JSON string to the file
        file.write(json_string)


# def load_q(agent):
#     loaded_data = {}
#     if os.path.exists(agent.file_name):
#         # Open the JSON file in read mode
#         with open(agent.file_name, 'r') as f:
#             loaded_str_data = ujson.load(f)
#         # Convert string keys back to tuples
#         loaded_data = {eval(key): value for key, value in loaded_str_data.items()}
#         return loaded_data
#     else:
#         return loaded_data

def load_q(agent):
    loaded_data = {}
    if os.path.exists(agent.file_name):
        # Open the file in read mode
        with open(agent.file_name, 'r') as f:
            # Read the entire file into a string
            file_content = f.read()
        # Use loads to convert the string into a Python object
        loaded_str_data = ujson.loads(file_content)
        # Convert string keys back to tuples
        loaded_data = {eval(key): value for key, value in loaded_str_data.items()}
        return loaded_data
    else:
        return loaded_data

# def load_q_for_board(agent, board_fen):
#     loaded_data = {}
#     if os.path.exists(agent.file_name):
#         # Open the JSON file
#         with open(agent.file_name, 'r') as json_file:
#             # Create an iterator for parsing the JSON
#             parser = ijson.items(json_file, '')
#
#             # Create an empty dictionary to store the matching entries
#             filtered_entries = {}
#
#             # Iterate over the parser events
#             for item in parser:
#                 # Iterate over the keys in the item
#                 for key in item.keys():
#                     # Check if the key contains the desired substring
#                     if board_fen in key:
#                         # Add the matching entry to the dictionary
#                         filtered_entries[key] = item[key]
#             # Convert string keys back to tuples
#             loaded_data = {eval(key): value for key, value in filtered_entries.items()}
#             agent.q_values = loaded_data
