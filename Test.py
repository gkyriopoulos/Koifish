import random
import time

import Engine


def main():
    total_moves = 0
    num_episodes = 1000
    board_choice = "Normal"
    start_time = time.time()
    for episode in range(num_episodes):
        my_engine = Engine.Engine(board_choice)
        while my_engine.winner == "None":
            random_move = random.choice(my_engine.legal_moves)
            my_engine.attempt_move(random_move[0], random_move[1], my_engine.turn_player)
        total_moves += my_engine.moves
    end_time = time.time()
    total_time = end_time - start_time
    moves_per_sec = total_moves/total_time
    print("Moves per sec:", moves_per_sec)

if __name__ == "__main__":
    main()
