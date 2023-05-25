class Engine:
	def __init__(self, board):
		self.board = board
		self.white_moves = True

	def print_board(self):
		print(self.board)

class Piece:
	def __init__(self,id,color,type):
		self.id = id
		self.color = color
		self.type = type
