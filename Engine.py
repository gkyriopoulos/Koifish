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
        ["br", "**", "**", "**", "bk", "**", "**", "br"],
        ["wq", "**", "**", "**", "**", "**", "**", "wq"],
        ["**", "**", "**", "**", "**", "**", "**", "**"],
        ["**", "**", "**", "**", "**", "**", "**", "**"],
        ["**", "**", "**", "**", "**", "**", "**", "**"],
        ["**", "**", "**", "**", "**", "**", "**", "**"],
        ["bq", "**", "**", "**", "**", "**", "**", "bq"],
        ["wr", "**", "**", "**", "wk", "**", "**", "wr"]]

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
            self.king_b_moved = False
            self.king_w_moved = False
            self.rook_small_w_moved = False
            self.rook_big_w_moved = False
            self.rook_small_b_moved = False
            self.rook_big_b_moved = False
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
            self.king_b_moved = False
            self.king_w_moved = False
            self.rook_small_w_moved = False
            self.rook_big_w_moved = False
            self.rook_small_b_moved = False
            self.rook_big_b_moved = False
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
            self.king_b_moved = False
            self.king_w_moved = False
            self.rook_small_w_moved = False
            self.rook_big_w_moved = False
            self.rook_small_b_moved = False
            self.rook_big_b_moved = False

        # TODO: We have to create a function that checks the board and calculates the score in case you
        #  start with handicap, just and idea for now.
        self.pieces = ["r", "n", "b", "q", "k", "p"]
        self.score = 0
        self.turn_player = "w"
        self.pseudolegal_moves = []
        self.legal_moves = []
        self.threatmap = []
        self.generate_legal_moves(self.turn_player)
        # I use this to player swap in player vs player mode it's probably not need.
        self.board_has_changed = False

    # TODO: Type moves dont work for now but it's an easy fix though
    def type_move(self, src, dst, player):
        return self._make_move(self._convert_type_move(src), self._convert_type_move(dst), player)

    def _convert_type_move(self, move):
        move_x = self._microChessMoves[move][0]
        move_y = self._microChessMoves[move][1]
        return [move_y, move_x]

    def attempt_move(self, src, dst, player):
        # print(self.legal_moves)
        # print(src, dst)

        if (src, dst) in self.legal_moves:
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

        if player == "w":
            if self.is_king(src):
                self._set_king_pos(dst, player)
                self.king_w_moved = True
            if self.is_rook(src):
                if src == self.rook_small_w:
                    self.rook_small_w_moved = True
                if src == self.rook_big_w:
                    self.rook_big_w_moved = True
        else:
            if self.is_king(src):
                self._set_king_pos(dst, player)
                self.king_b_moved = True
            if self.is_rook(src):
                if src == self.rook_small_b:
                    self.rook_small_b_moved = True
                if src == self.rook_big_b:
                    self.rook_big_b_moved = True

        if src == (0, 4) and dst == (0, 7):
            self.board[src[0]][src[1]] = "**"
            self.board[dst[0]][dst[1]] = "**"
            self.board[0][6] = "bk"
            self.board[0][5] = "br"
            self._set_king_pos((0, 6), "b")
            self.king_b_moved = True
        elif src == (0, 4) and dst == (0, 0):
            self.board[src[0]][src[1]] = "**"
            self.board[dst[0]][dst[1]] = "**"
            self.board[0][2] = "bk"
            self.board[0][3] = "br"
            self._set_king_pos((0, 2), "b")
            self.king_b_moved = True
        elif src == (7, 4) and dst == (7, 7):
            self.board[src[0]][src[1]] = "**"
            self.board[dst[0]][dst[1]] = "**"
            self.board[7][6] = "wk"
            self.board[7][5] = "wr"
            self._set_king_pos((7, 6), "w")
            self.king_w_moved = True
        elif src == (7, 4) and dst == (7, 0):
            self.board[src[0]][src[1]] = "**"
            self.board[dst[0]][dst[1]] = "**"
            self.board[7][2] = "wk"
            self.board[7][3] = "wr"
            self._set_king_pos((7, 2), "w")
            self.king_w_moved = True
        else:
            self.board[dst[0]][dst[1]] = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = "**"

        # Swaps the player and calculates legal moves for the next player.
        self.turn_player = "b" if self.turn_player == "w" else "w"
        self.board_has_changed = True
        self.pseudolegal_moves.clear()
        self.threatmap.clear()
        self.legal_moves.clear()
        # Note: If you change the position of generate legal moves you will have issue with pawns and checks because
        # you move the pawn and then check for a check BE CAREFUL!
        self.generate_legal_moves(self.turn_player)
        return self.board

    def generate_legal_moves(self, color):
        self._generate_pseudolegal_moves(color)
        self.legal_moves.append(self.pseudolegal_moves)

        king_moves = self._get_king_moves(self._get_king_pos(color), color)
        set_king_moves = set([x[1] for x in self._get_king_moves(self._get_king_pos(color), color)])
        set_threatmap = set(self.threatmap)
        king_illegal_moves = [i for i in king_moves if i[1] in (set_king_moves & set_threatmap)]

        # Removing king's illegal moves.
        self.legal_moves = list(set(self.pseudolegal_moves) - set(king_illegal_moves))

        # Gia ta pinned tha pernw thn thesi tous kai tha
        # kanw remove apo to legal_moves osa exoun src to src tou pinned

        castle_big_move = self._check_big_castle(color)
        castle_small_move = self._check_small_castle(color)

        self.legal_moves.append(castle_small_move)
        self.legal_moves.append(castle_big_move)

        checkers = self._check_check(color)
        if len(checkers) > 1:
            king_legal_moves = [i for i in king_moves if i[1] not in (set_king_moves & set_threatmap)]
            self.legal_moves = king_legal_moves
            if not self.legal_moves:
                print("Checkmate")
        elif len(checkers) == 1:
            if not self.legal_moves:
                print("Checkmate")
        # else:
        #     # Flatten the list
        #     self.legal_moves = list(itertools.chain(*self.legal_moves))
        # Remove empty moves

        self.legal_moves = [x for x in self.legal_moves if x]

        if not self.legal_moves:
            print("Stalemate")

    def _generate_pseudolegal_moves(self, color):
        for i in range(self.dim_x):
            for j in range(self.dim_y):
                piece_color = self.get_color((j, i))
                enemy_color = "b" if color == "w" else "w"
                if piece_color == color:
                    moves = self._get_moves((j, i), color)
                    self.pseudolegal_moves.append(moves)
                elif piece_color == enemy_color:
                    threatmap = self._get_threatmap((j, i), piece_color)
                    self.threatmap.append(threatmap)

        # Remove empty moves
        self.pseudolegal_moves = [x for x in self.pseudolegal_moves if x]
        self.threatmap = [x for x in self.threatmap if x]
        # Flatten the list of moves
        self.pseudolegal_moves = list(itertools.chain(*self.pseudolegal_moves))
        self.threatmap = list(itertools.chain(*self.threatmap))
        # Getting ONLY the dst coordinate.
        self.threatmap = [threat[1] for threat in self.threatmap]
        # Removing duplicate threats
        self.threatmap.sort()
        grouped = itertools.groupby(self.threatmap)
        self.threatmap = [key for key, _ in grouped]

    # Access a location on the board finds if there is a piece on it and depending on the piece's type
    # get its moves it also returns the threat-map for each piece (ray pieces(rook,bishop)) use a different function
    # for the threat-map calculation
    def _get_moves(self, src, color):
        if self.is_pawn((src[0], src[1])):
            return self._get_pawn_moves((src[0], src[1]), color)
        elif self.is_rook((src[0], src[1])):
            return self._get_rook_moves((src[0], src[1]), color)
        elif self.is_knight((src[0], src[1])):
            return self._get_knight_moves((src[0], src[1]), color)
        elif self.is_bishop((src[0], src[1])):
            return self._get_bishop_moves((src[0], src[1]), color)
        elif self.is_king((src[0], src[1])):
            return self._get_king_moves((src[0], src[1]), color)
        elif self.is_queen((src[0], src[1])):
            return self._get_queen_moves((src[0], src[1]), color)

    # Theoretically finds a piece's moves given its location. This function doesn't use the board.
    # Think of as: If I place a piece on (y,x) square what would be the available moves ?
    def get_pieces_moves(self, src, piece, color):
        if piece == "p":
            return self._get_pawn_moves(src, color)
        if piece == "b":
            return self._get_bishop_moves(src, color)
        if piece == "n":
            return self._get_knight_moves(src, color)
        if piece == "r":
            return self._get_rook_moves(src, color)
        if piece == "q":
            return self._get_queen_moves(src, color)
        if piece == "k":
            return self._get_king_moves(src, color)

    # TODO: EN PASSANT CHANGES THE MOVES FOR THE PAWNS CARE!!!!!!!!!
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
                            (calc_y, calc_x)) != color:
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
                            (calc_y, calc_x)) != color:
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
        return moves

    def _get_rook_moves(self, src, color):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # Dim_y is chosen here because it is the biggest dimension
        # it requires some thought in order to be clear why it is like that
        # Hint: The line that a rook moves on is infinitely big
        biggest_dim = self.dim_y if self.dim_y >= self.dim_x else self.dim_x
        for d in directions:
            for i in range(1, biggest_dim):
                calc_y = src[0] + i * d[0]
                calc_x = src[1] + i * d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    if self.get_piece([calc_y, calc_x]) == "*":
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    elif self.get_color([calc_y, calc_x]) != color:
                        # If an enemy piece is found in this direction break and check another direction
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def _get_knight_moves(self, src, color):
        moves = []
        directions = [(-2, -1), (-1, -2), (2, -1), (1, -2), (2, 1), (1, 2), (-2, 1), (-1, 2)]
        for d in directions:
            calc_y = src[0] + d[0]
            calc_x = src[1] + d[1]
            if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                # Knight only cares about the landing square
                if self.get_color([calc_y, calc_x]) != color:
                    moves.append(((src[0], src[1]), (calc_y, calc_x)))
        return moves

    # Same as rook only thing that changes is the direction of motion.
    def _get_bishop_moves(self, src, color):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        biggest_dim = self.dim_y if self.dim_y >= self.dim_x else self.dim_x
        for d in directions:
            for i in range(1, biggest_dim):
                calc_y = src[0] + i * d[0]
                calc_x = src[1] + i * d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    if self.get_piece([calc_y, calc_x]) == "*":
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                    elif self.get_color([calc_y, calc_x]) != color:
                        # If an enemy piece is found in this direction break and check another direction
                        moves.append(((src[0], src[1]), (calc_y, calc_x)))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def _get_king_moves(self, src, color):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            calc_y = src[0] + d[0]
            calc_x = src[1] + d[1]
            if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                if self.get_color([calc_y, calc_x]) != color:
                    moves.append(((src[0], src[1]), (calc_y, calc_x)))
        return moves

    def _get_queen_moves(self, src, color):
        moves = [self._get_rook_moves(src, color), self._get_bishop_moves(src, color)]
        # Remove empty moves
        moves = [x for x in moves if x]
        # Flatten the list of moves
        moves = list(itertools.chain(*moves))
        return moves

    # Threat maps for non ray pieces are the same as their moves except pawns
    # because the only capture diagonally.
    def _get_threatmap(self, src, color):
        if self.is_pawn((src[0], src[1])):
            return self._get_pawn_threatmap((src[0], src[1]), color)
        elif self.is_rook((src[0], src[1])):
            return self._get_rook_threatmap((src[0], src[1]), color)
        elif self.is_knight((src[0], src[1])):
            return self._get_knight_threatmap((src[0], src[1]), color)
        elif self.is_bishop((src[0], src[1])):
            return self._get_bishop_threatmap((src[0], src[1]), color)
        elif self.is_king((src[0], src[1])):
            return self._get_king_threatmap((src[0], src[1]), color)
        elif self.is_queen((src[0], src[1])):
            return self._get_queen_threatmap((src[0], src[1]), color)

    # TODO: EN PASSANT CHANGES THE THREATMAP FOR THE PAWNS CARE!!!!!!!!!
    def _get_pawn_threatmap(self, src, color):
        threatmap = []
        if color == "w":
            directions = [(-1, -1), (-1, 1)]
            for d in directions:
                calc_y = src[0] + d[0]
                calc_x = src[1] + d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    # Append regardless of the square
                    threatmap.append(((src[0], src[1]), (calc_y, calc_x)))
        else:
            directions = [(1, -1), (1, 1)]
            for d in directions:
                calc_y = src[0] + d[0]
                calc_x = src[1] + d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    threatmap.append(((src[0], src[1]), (calc_y, calc_x)))
        return threatmap

    def _get_rook_threatmap(self, src, color):
        # Getting enemy kings coords
        if color == "w":
            temp_king = self.king_pos_b
            piece = "bk"
        else:
            temp_king = self.king_pos_w
            piece = "wk"
        # Temporarily removing enemy king from the board
        self.board[temp_king[0]][temp_king[1]] = "**"
        # Getting our moves.
        threatmap = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # Dim_y is chosen here because it is the biggest dimension
        # it requires some thought in order to be clear why it is like that
        # Hint: The line that a rook moves on is infinitely big
        biggest_dim = self.dim_y if self.dim_y >= self.dim_x else self.dim_x
        for d in directions:
            for i in range(1, biggest_dim):
                calc_y = src[0] + i * d[0]
                calc_x = src[1] + i * d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    if self.get_piece([calc_y, calc_x]) == "*":
                        threatmap.append(((src[0], src[1]), (calc_y, calc_x)))
                    # If a piece is found regardless of color it's intended trust me.
                    elif self.get_color([calc_y, calc_x]) != "*":
                        threatmap.append(((src[0], src[1]), (calc_y, calc_x)))
                        break
                    else:
                        break
                else:
                    break
        # Restoring enemy king to his original place
        self.board[temp_king[0]][temp_king[1]] = piece
        return threatmap

    def _get_knight_threatmap(self, src, color):
        threatmap = []
        directions = [(-2, -1), (-1, -2), (2, -1), (1, -2), (2, 1), (1, 2), (-2, 1), (-1, 2)]
        for d in directions:
            calc_y = src[0] + d[0]
            calc_x = src[1] + d[1]
            if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                # Knight only cares about the landing square
                threatmap.append(((src[0], src[1]), (calc_y, calc_x)))
        return threatmap

    # Same as get rook threatmap
    def _get_bishop_threatmap(self, src, color):
        if color == "w":
            temp_king = self.king_pos_b
            piece = "bk"
        else:
            temp_king = self.king_pos_w
            piece = "wk"
        self.board[temp_king[0]][temp_king[1]] = "**"
        threatmap = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        biggest_dim = self.dim_y if self.dim_y >= self.dim_x else self.dim_x
        for d in directions:
            for i in range(1, biggest_dim):
                calc_y = src[0] + i * d[0]
                calc_x = src[1] + i * d[1]
                if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                    if self.get_piece([calc_y, calc_x]) == "*":
                        threatmap.append(((src[0], src[1]), (calc_y, calc_x)))
                    elif self.get_color([calc_y, calc_x]) != "*":
                        # If an enemy piece is found in this direction break and check another direction
                        threatmap.append(((src[0], src[1]), (calc_y, calc_x)))
                        break
                    else:
                        break
                else:
                    break
        self.board[temp_king[0]][temp_king[1]] = piece
        return threatmap

    def _get_king_threatmap(self, src, color):
        threatmap = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            calc_y = src[0] + d[0]
            calc_x = src[1] + d[1]
            if 0 <= calc_y < self.dim_y and 0 <= calc_x < self.dim_x:
                threatmap.append(((src[0], src[1]), (calc_y, calc_x)))
        return threatmap

    def _get_queen_threatmap(self, src, color):
        threatmap = [self._get_rook_threatmap(src, color), self._get_bishop_threatmap(src, color)]
        threatmap = [x for x in threatmap if x]
        threatmap = list(itertools.chain(*threatmap))
        return threatmap

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

    def _check_small_castle(self, color):
        if color == "w":
            if self._small_castle_available(color):
                if (7, 4) not in self.threatmap and \
                        (7, 5) not in self.threatmap and \
                        (7, 6) not in self.threatmap:
                    return (7, 4), (7, 7)
                else:
                    return []
            else:
                return []
        else:
            if self._small_castle_available(color):
                if (0, 4) not in self.threatmap and \
                        (0, 5) not in self.threatmap and \
                        (0, 6) not in self.threatmap:
                    return (0, 4), (0, 7)
                else:
                    return []
            else:
                return []

    def _check_big_castle(self, color):
        if color == "w":
            if self._big_castle_available(color):
                if (7, 4) not in self.threatmap and \
                        (7, 1) not in self.threatmap and \
                        (7, 2) not in self.threatmap and \
                        (7, 3) not in self.threatmap:
                    return (7, 4), (7, 0)
                else:
                    return []
            else:
                return []
        else:
            if self._big_castle_available(color):
                if (0, 4) not in self.threatmap and \
                        (0, 1) not in self.threatmap and \
                        (0, 2) not in self.threatmap and \
                        (0, 3) not in self.threatmap:
                    return (0, 4), (0, 0)
                else:
                    return []
            else:
                return []

    def _big_castle_available(self, color):
        if color == "w":
            if not self.king_w_moved and not self.rook_big_w_moved and \
                    self.board[7][1] == "**" and self.board[7][2] == "**" \
                    and self.board[7][3] == "**":
                return True
            else:
                return False
        else:
            if not self.king_b_moved and not self.rook_big_b_moved and \
                    self.board[0][1] == "**" and self.board[0][2] == "**" \
                    and self.board[0][3] == "**":
                return True
            else:
                return False

    def _small_castle_available(self, color):
        if color == "w":
            if not self.king_w_moved and not self.rook_small_w_moved and \
                    self.board[7][5] == "**" and self.board[7][6] == "**":
                return True
            else:
                return False
        else:
            if not self.king_b_moved and not self.rook_small_b_moved and \
                    self.board[0][5] == "**" and self.board[0][6] == "**":
                return True
            else:
                return False

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

    def _get_king_pos(self, color):
        return self.king_pos_b if color == "b" else self.king_pos_w

    # TODO: Castling done testing left.
    # TODO: If in check limit moves. Or if in double check only king can move.
    # TODO: Pins.
    # TODO: En-passant and en-passant checks.
    # TODO: Repetition stalemates and stuff.
