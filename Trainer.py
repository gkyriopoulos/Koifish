#!/usr/bin/env python3
import sys
import time
import ujson
from matplotlib import pyplot as plt

import Agent


def main():
    if len(sys.argv) != 3:
        print("Please provide the board and the episodes as a command-line argument.")
        return

    board = sys.argv[1]
    episodes = int(sys.argv[2])

    train(board, episodes, False, True, True, True)


def train(board, episodes, plot, save, train_w, train_b):
    avg_reward_w = []
    avg_reward_b = []
    wr_w = 0
    wr_b = 0
    time_w = 0
    time_b = 0

    if train_w:
        start_time1 = time.time()
        avg_reward_w, wr_w = Agent.train_agent_vs_random(board, episodes, "w")
        end_time1 = time.time()
        time_w = end_time1 - start_time1

    if train_b:
        start_time2 = time.time()
        avg_reward_b, wr_b = Agent.train_agent_vs_random(board, episodes, "b")
        end_time2 = time.time()
        time_b = end_time2 - start_time2

    # start_time3.append(time.time())
    # Agent.train_agent_vs_agent(tb, episodes)
    # end_time3.append(time.time())

    # times_agent_3 = numpy.subtract(end_time3, start_time3).tolist()

    if plot:
        plt.semilogy(avg_reward_w, label="White Reward, T = " + str(episodes))
        plt.semilogy(avg_reward_b, label="Black Reward, T = " + str(episodes))
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Average Reward")
        plt.show()

    if save:
        folder = 'stats'
        graph_file = folder + '/' + board + "_graph" + ".stats"
        wr_file = folder + '/' + board + "_wr" + ".stats"
        time_file = folder + '/' + board + "_time" + ".stats"

        with open(graph_file, 'a+') as file:
            if train_w:
                file.write(ujson.dumps(avg_reward_w.tolist()))
                file.write('\n')
            if train_b:
                file.write(ujson.dumps(avg_reward_b.tolist()))
                file.write('\n')
            file.write('\n')
        with open(wr_file, 'a+') as file:
            if train_w:
                file.write(str(wr_w) + '\n')
            if train_b:
                file.write(str(wr_b) + '\n')
            file.write('\n')
        with open(time_file, 'a+') as file:
            if train_w:
                file.write(str(time_w) + '\n')
            if train_b:
                file.write(str(time_b) + '\n')
            file.write('\n')


if __name__ == "__main__":
    main()
