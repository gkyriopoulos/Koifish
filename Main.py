import pygame as pg
import Engine

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

boardMinichess = [
	["bk", "bn", "bb", "br"],
	["bp", "**", "**", "**"],
	["**", "**", "**", "**"],
	["**", "**", "**", "wp"],
	["wr", "wb", "wn", "wk"]]


def main():

	selected_board = boardMinichess
	print("Hello world!")


if __name__ == "__main__":
	main()

