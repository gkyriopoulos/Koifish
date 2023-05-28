import itertools


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

    _boardTest = [
        ["bk", "**", "**", "**"],
        ["bp", "bp", "**", "**"],
        ["**", "**", "**", "**"],
        ["**", "**", "wp", "wp"],
        ["**", "**", "**", "wk"]]

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
            self.king_pos_b = [0, 0]
            self.king_pos_w = [4, 3]
            self.rook_small_w = None
            self.rook_big_w = (4, 0)
            self.rook_small_b = None
            self.rook_big_b = (0, 3)
        elif board_choice == "LosAlamos":
            self.board = self._boardLosAlamos
            self.dim_x = 6
            self.dim_y = 6
            self.king_pos_b = [0, 3]
            self.king_pos_w = [5, 3]
            self.rook_small_w = (5, 5)
            self.rook_big_w = (5, 0)
            self.rook_small_b = (0, 5)
            self.rook_big_b = (0, 0)
        else:
            self.board = self._boardNormal
            self.dim_x = 8
            self.dim_y = 8
            self.king_pos_b = [0, 4]
            self.king_pos_w = [7, 4]
            self.rook_small_w = (7, 7)
            self.rook_big_w = (7, 0)
            self.rook_small_b = (0, 7)
            self.rook_big_b = (0, 0)

        # TODO: We have to create a function that checks the board and calculates the score in case you
        #  start with handicap, just and idea for now.
        self.score = 0
        self.turn_player = "w"
        self.available_moves = []
        self._generate_available_moves()
        # I use this to player swap in player vs player mode it's probably not need.
        self.board_has_changed = False
        self.pieces = ["r", "n", "b", "q", "k", "p"]

    # TODO: Type moves dont work for now but it's an easy fix though
    def type_move(self, src, dst, player):
        return self._make_move(self._convert_type_move(src), self._convert_type_move(dst), player)

    def _convert_type_move(self, move):
        move_x = self._microChessMoves[move][0]
        move_y = self._microChessMoves[move][1]
        return [move_y, move_x]

    def attempt_move(self, src, dst, player):
        # TODO: Change to .legal_moves
        if (src, dst) in self.available_moves:
            self._make_move(src, dst, player)
            return self.board
        else:
            self.board_has_changed = False
            return self.board

    def _make_move(self, src, dst, player):

        if player != self.turn_player:
            print("It's not your turn yet.")
            self.board_has_changed = False
            return self.board

        if self.is_king(src):
            self._set_king_pos(dst, player)

        self.board[dst[0]][dst[1]] = self.board[src[0]][src[1]]
        self.board[src[0]][src[1]] = "**"

        # Swaps the player and calculates legal moves for the next player.
        self.turn_player = "b" if self.turn_player == "w" else "w"
        self.board_has_changed = True
        self.available_moves.clear()
        # Note: If you change the position of generate legal moves you will have issue with pawns and checks because
        # you move the pawn and then check for a check BE CAREFUL!
        self.generate_legal_moves()
        return self.board

    def generate_legal_moves(self):
        print(self.turn_player)
        self._generate_available_moves()
        checkers = self._check_check(self.turn_player)
        print(checkers)

    def _generate_available_moves(self):
        for i in range(self.dim_x):
            for j in range(self.dim_y):
                color = self.get_color((j, i))
                if color == self.turn_player:
                    moves = self._get_moves((j, i))
                    self.available_moves.append(moves)
        # Remove empty moves
        self.available_moves = [x for x in self.available_moves if x]
        # Flatten the list of moves
        self.available_moves = list(itertools.chain(*self.available_moves))

    # Access a location on the board finds if there is a piece on it and depending on the piece's type
    # get its moves
    def _get_moves(self, src):
        color = self.get_color((src[0], src[1]))
        if self.is_pawn((src[0], src[1])):
            return self._get_pawn_moves((src[0], src[1]), color)
        elif self.is_rook((src[0], src[1])):
            return self._get_rook_moves((src[0], src[1]))
        elif self.is_knight((src[0], src[1])):
            return self._get_knight_moves((src[0], src[1]))
        elif self.is_bishop((src[0], src[1])):
            return self._get_bishop_moves((src[0], src[1]))
        elif self.is_king((src[0], src[1])):
            return self._get_king_moves((src[0], src[1]))
        elif self.is_queen((src[0], src[1])):
            return self._get_queen_moves((src[0], src[1]))

    # Theoretically finds a piece's moves given it's location. This function doesn't use the board.
    # Think of as: If I place a piece on (y,x) square what would be the available moves ?
    def get_pieces_moves(self, src, piece, color):
        if piece == "p":
            return self._get_pawn_moves(src, color)
        if piece == "b":
            return self._get_bishop_moves(src)
        if piece == "n":
            return self._get_knight_moves(src)
        if piece == "r":
            return self._get_rook_moves(src)
        if piece == "q":
            return self._get_queen_moves(src)
        if piece == "k":
            return self._get_king_moves(src)

    def _get_pawn_moves(self, src, color):
        moves = []
        if color == "w":
            directions = [(-1, -1), (-1, 0), (-2, 0), (-1, 1)]
            for d in directions:
                calc_y = src[0] + d[0]
                calc_x = src[1] + d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    if d == (-1, 0) and self.get_piece((calc_y, calc_x)) == "*":
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    if d == (-2, 0) and self.get_piece((calc_y, calc_x)) == "*" and src[0] == (self.dim_y - 1) - 1:
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    if (d == (-1, -1) or d == (-1, 1)) and self.get_piece((calc_y, calc_x)) != "*" and self.get_color(
                            (calc_y, calc_x)) != self.turn_player:
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
        else:
            directions = [(1, -1), (1, 0), (2, 0), (1, 1)]
            for d in directions:
                calc_y = src[0] + d[0]
                calc_x = src[1] + d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    if d == (1, 0) and self.get_piece((calc_y, calc_x)) == "*":
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    if d == (2, 0) and self.get_piece((calc_y, calc_x)) == "*" and src[0] == 1:
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    if (d == (1, -1) or d == (1, 1)) and self.get_piece((calc_y, calc_x)) != "*" and self.get_color(
                            (calc_y, calc_x)) != self.turn_player:
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
        return moves

    def _get_rook_moves(self, src):
        moves = []
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
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    elif self.get_color([calc_y, calc_x]) != self.turn_player:
                        # If an enemy piece is found in this direction break and check another direction
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def _get_knight_moves(self, src):
        moves = []
        directions = [(-2, -1), (-1, -2), (2, -1), (1, -2), (2, 1), (1, 2), (-2, 1), (-1, 2)]
        for d in directions:
            calc_y = src[0] + d[0]
            calc_x = src[1] + d[1]
            if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                # Knight only cares about the landing square
                if self.get_color([calc_y, calc_x]) != self.turn_player:
                    moves.append(((src[0], src[1]), (calc_y, calc_x)))
        return moves

    # Same as rook only thing that changes is the direction of motion.
    def _get_bishop_moves(self, src):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            for i in range(1, self.dim_y):
                calc_y = src[0] + i * d[0]
                calc_x = src[1] + i * d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    if self.get_piece([calc_y, calc_x]) == "*":
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    elif self.get_color([calc_y, calc_x]) != self.turn_player:
                        # If an enemy piece is found in this direction break and check another direction
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def _get_king_moves(self, src):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            calc_y = src[0] + d[0]
            calc_x = src[1] + d[1]
            if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                if self.get_color([calc_y, calc_x]) != self.turn_player:
                    moves.append(((src[0], src[1]), (calc_y, calc_x)))
        return moves

    def _get_queen_moves(self, src):
        moves = [self._get_rook_moves(src), self._get_bishop_moves(src)]
        # Remove empty moves
        moves = [x for x in moves if x]
        # Flatten the list of moves
        moves = list(itertools.chain(*moves))
        return moves

    # Just check's if there is a check I thought I sounded funny xD
    # Check is the player->color has any checks. And returns checking piece's position.
    def _check_check(self, color):
        king_pos = self.king_pos_w if color == "w" else self.king_pos_b
        checkers = []
        for piece in self.pieces:
            moves = self.get_pieces_moves(king_pos, piece, color)
            for move in moves:
                if self.get_piece(move[1]) == piece:
                    checkers.append(move[1])
        return checkers

    def get_color(self, src):
        return self.board[src[0]][src[1]][0]

    def get_piece(self, src):
        return self.board[src[0]][src[1]][1]

    def is_king(self, src):
        return True if self.get_piece((src[0], src[1])) == "k" else False

    def is_queen(self, src):
        return True if self.get_piece((src[0], src[1])) == "q" else False

    def is_rook(self, src):
        return True if self.get_piece((src[0], src[1])) == "r" else False

    def is_bishop(self, src):
        return True if self.get_piece((src[0], src[1])) == "b" else False

    def is_knight(self, src):
        return True if self.get_piece((src[0], src[1])) == "n" else False

    def is_pawn(self, src):
        return True if self.get_piece((src[0], src[1])) == "p" else False

    def _set_king_pos(self, src, color):
        if color == "w":
            self.king_pos_w = src
        else:
            self.king_pos_b = src

    # TODO: If in check limit moves. Or if in double check only king can move.
    # TODO: Pins.
    # TODO: Castling.
    # TODO: En-passant and en-passant checks.
