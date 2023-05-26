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
        "a1": [0, 4], "a2": [0, 3], "a3": [0, 2], "a4": [0, 1], "a5": [0, 0],
        "b1": [1, 4], "b2": [1, 3], "b3": [1, 2], "b4": [1, 1], "b5": [1, 0],
        "c1": [2, 4], "c2": [2, 3], "c3": [2, 2], "c4": [2, 1], "c5": [2, 0],
        "d1": [3, 4], "d2": [3, 3], "d3": [3, 2], "d4": [3, 1], "d5": [3, 0]}

    def __init__(self, board_choice):
        if board_choice == "MicroChess":
            self.board = self._boardMicroChess
        elif board_choice == "LosAlamos":
            self.board = self._boardLosAlamos
        else:
            self.board = self._boardNormal

        self.white_moves = True

    def move(self, curr, dest):
        curr_x, curr_y = self._convert_move(curr)
        dest_x, dest_y = self._convert_move(dest)

        self.board[dest_y][dest_x] = self.board[curr_y][curr_x]
        self.board[curr_y][curr_x] = "**"

        return self.board

    def _convert_move(self, move):
        move_x = self._microChessMoves[move][0]
        move_y = self._microChessMoves[move][1]
        return move_x, move_y
