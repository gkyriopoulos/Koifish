import pygame as pg
import Engine as egn

board = [
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

boardMiniChess = [
	["bk", "bn", "bb", "br"],
	["bp", "**", "**", "**"],
	["**", "**", "**", "**"],
	["**", "**", "**", "wp"],
	["wr", "wb", "wn", "wk"]]


def main():

	selected_board = boardMiniChess
	board = egn.Engine(selected_board)
	board.print_board()


if __name__ == "__main__":
	main()
