import random
import time

import numpy

import Engine


def main():
    # total_moves = 0
    # num_episodes = 10000
    # board_choice = "MicroChess"
    # start_time = time.time()
    # for episode in range(num_episodes):
    #     my_engine = Engine.Engine(board_choice)
    #     while my_engine.winner == "None":
    #         random_move = random.choice(my_engine.legal_moves)
    #         my_engine.attempt_move(random_move[0], random_move[1], my_engine.turn_player)
    #     total_moves += my_engine.moves
    # end_time = time.time()
    # total_time = end_time - start_time
    # moves_per_sec = total_moves/total_time
    # print("Moves per sec:", moves_per_sec)

    list1 = [1, 2, 3, 4, 5, 6]
    list2 = [-1, -2, -3, -4, -5, -6]

    lista = numpy.subtract(list1, list2).tolist()
    print(lista)


if __name__ == "__main__":
    main()
