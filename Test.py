import random
import time

import Engine
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor


def play_episode(board_choice):
    my_engine = Engine.Engine(board_choice)
    while my_engine.winner == "None":
        random_move = random.choice(my_engine.legal_moves)
        my_engine.attempt_move(random_move[0], random_move[1], my_engine.turn_player)
    return my_engine.moves


def main():
    total_moves = 0
    num_episodes = 10000
    board_choice = "MicroChess"
    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        episode_results = executor.map(play_episode, [board_choice] * num_episodes)
        total_moves = sum(episode_results)

    end_time = time.time()
    total_time = end_time - start_time
    moves_per_sec = total_moves / total_time
    print("Moves per sec:", moves_per_sec)


if __name__ == "__main__":
    main()
