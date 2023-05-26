def _remove_duplicates(alist):
    return list(set(alist))


class Engine:
    _boardNormal = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["**", "**", "**", "**", "**", "**", "**", "**"],
        ["**", "**", "**", "**", "**", "**", "**", "**"],
        ["**", "**", "**", "**", "**", "**", "**", "**"],
        ["**", "**", "**", "**", "**", "**", "**", "**"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]

    _boardLosAlamos = [
        ["br", "bn", "bq", "bk", "bn", "br"],
        ["bp", "bp", "bp", "bp", "bp", "bp"],
        ["**", "**", "**", "**", "**", "**"],
        ["**", "**", "**", "**", "**", "**"],
        ["wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wq", "wk", "wn", "wr"]]

    _boardMicroChess = [
        ["bk", "bn", "bb", "br"],
        ["bp", "**", "**", "**"],
        ["**", "**", "**", "**"],
        ["**", "**", "**", "wp"],
        ["wr", "wb", "wn", "wk"]]

    _microChessMoves = {
        "a1": (0, 4), "a2": (0, 3), "a3": (0, 2), "a4": (0, 1), "a5": (0, 0),
        "b1": (1, 4), "b2": (1, 3), "b3": (1, 2), "b4": (1, 1), "b5": (1, 0),
        "c1": (2, 4), "c2": (2, 3), "c3": (2, 2), "c4": (2, 1), "c5": (2, 0),
        "d1": (3, 4), "d2": (3, 3), "d3": (3, 2), "d4": (3, 1), "d5": (3, 0)}

    def __init__(self, board_choice):

        if board_choice == "MicroChess":
            self.board = self._boardMicroChess
            self.dim_x = 4
            self.dim_y = 5
        elif board_choice == "LosAlamos":
            self.board = self._boardLosAlamos
            self.dim_x = 6
            self.dim_y = 6
        else:
            self.board = self._boardNormal
            self.dim_x = 8
            self.dim_y = 8

        # TODO: We have to create a function that checks the board and calculates the score in case you
        #  start with handicap, just and idea for now.
        self.score = 0
        self.turn_player = "w"
        self.pieces = []
        self.available_moves = []
        self.board_has_changed = False

    def type_move(self, src, dst, player):
        return self.make_move(self.convert_type_move(src), self.convert_type_move(dst), player)

    def convert_type_move(self, move):
        move_x = self._microChessMoves[move][0]
        move_y = self._microChessMoves[move][1]
        return [move_y, move_x]

    def attempt_move(self, src, dst, player):
        self.get_available_moves()
        print(self.available_moves)
        print((src, dst))
        if (src, dst) in self.available_moves:
            self.make_move(src, dst, player)
            return self.board
        else:
            self.board_has_changed = False
            return self.board

    def make_move(self, src, dst, player):

        if player != self.turn_player:
            print("It's not your turn yet.")
            self.board_has_changed = False
            return self.board
        # else:
        # self.get_available_moves()

        self.board[dst[0]][dst[1]] = self.board[src[0]][src[1]]
        self.board[src[0]][src[1]] = "**"

        self.turn_player = "b" if self.turn_player == "w" else "w"
        self.board_has_changed = True
        self.available_moves.clear()
        return self.board

    def get_available_moves(self):
        for i in range(self.dim_x):
            for j in range(self.dim_y):
                color = self.get_color([j, i])
                if color == self.turn_player:
                    if self.get_piece([j, i]) == "p":
                        self.get_pawn_moves([j, i], color)
                    elif self.get_piece([j, i]) == "r":
                        self.get_rook_moves([j, i])
                    elif self.get_piece([j, i]) == "n":
                        self.get_knight_moves([j, i])
                    elif self.get_piece([j, i]) == "b":
                        self.get_bishop_moves([j, i])
                    elif self.get_piece([j, i]) == "k":
                        self.get_king_moves([j, i])
                    elif self.get_piece([j, i]) == "q":
                        self.get_queen_moves([j, i])
        self.available_moves = _remove_duplicates(self.available_moves)

    def get_pawn_moves(self, src, color):
        return 1

    def get_rook_moves(self, src):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # Dim_y is chosen here because it is the biggest dimension
        # it requires some thought in order to be clear why it is like that
        # Hint: The line that a rook moves on is infinitely big
        for d in directions:
            for i in range(1, self.dim_y):
                calc_y = src[0] + i * d[0]
                calc_x = src[1] + i * d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    if self.get_piece([calc_y, calc_x]) == "*":
                        self.available_moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    elif self.get_color([calc_y, calc_x]) != self.turn_player:
                        # If an enemy piece is found in this direction break and check another direction
                        self.available_moves.append(((src[0], src[1]), (calc_y, calc_x)))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, src):
        directions = [(-2, -1), (-1, -2), (2, -1), (1, -2), (2, 1), (1, 2), (-2, 1), (-1, 2)]
        for d in directions:
            calc_y = src[0] + d[0]
            calc_x = src[1] + d[1]
            if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                # Knight only cares about the landing square
                if self.get_color([calc_y, calc_x]) != self.turn_player:
                    self.available_moves.append(((src[0], src[1]), (calc_y, calc_x)))

    # Same as rook only thing that changes is the direction of motion.
    def get_bishop_moves(self, src):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            for i in range(1, self.dim_y):
                calc_y = src[0] + i * d[0]
                calc_x = src[1] + i * d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    if self.get_piece([calc_y, calc_x]) == "*":
                        self.available_moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    elif self.get_color([calc_y, calc_x]) != self.turn_player:
                        # If an enemy piece is found in this direction break and check another direction
                        self.available_moves.append(((src[0], src[1]), (calc_y, calc_x)))
                        break
                    else:
                        break
                else:
                    break

    def get_king_moves(self, src):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            calc_y = src[0] + d[0]
            calc_x = src[1] + d[1]
            if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                if self.get_color([calc_y, calc_x]) != self.turn_player:
                    self.available_moves.append(((src[0], src[1]), (calc_y, calc_x)))

    def get_queen_moves(self, src):
        self.get_rook_moves(src)
        self.get_bishop_moves(src)

    def get_color(self, src):
        return self.board[src[0]][src[1]][0]

    def get_piece(self, src):
        return self.board[src[0]][src[1]][1]
