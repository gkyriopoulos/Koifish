#!/usr/bin/env python3
import sys
import time

import numpy as np
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
    bar_y_w = []
    bar_x_w = []
    bar_y_b = []
    bar_x_b = []
    wr_w = 0
    wr_b = 0
    time_w = 0
    time_b = 0

    if train_w:
        start_time1 = time.time()
        avg_reward_w, wr_w, bar_y_w, bar_x_w = Agent.train_agent_vs_random(board, episodes, "w")
        end_time1 = time.time()
        time_w = end_time1 - start_time1

    if train_b:
        start_time2 = time.time()
        avg_reward_b, wr_b, bar_y_b, bar_x_b = Agent.train_agent_vs_random(board, episodes, "b")
        end_time2 = time.time()
        time_b = end_time2 - start_time2


    if plot:
        learning_curve_plot(episodes, avg_reward_w, avg_reward_b)
        if train_w:
            bar_plot(bar_x_w, bar_y_w)
        if train_b:
            bar_plot(bar_x_b, bar_y_b)

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


def learning_curve_plot(episodes, avg_reward_w, avg_reward_b):
    plt.semilogy(avg_reward_w, label="White Reward, T = " + str(episodes))
    plt.semilogy(avg_reward_b, label="Black Reward, T = " + str(episodes))
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Average Reward")
    plt.show()


def bar_plot(bar_x, bar_y):
    print([item[0] for item in bar_y])
    print([item[1] for item in bar_y])
    print([item[2] for item in bar_y])

    # set width of bar
    barwidth = 0.25
    fig = plt.subplots(figsize=(12, 8))

    # set height of bar
    white = [item[0] for item in bar_y]
    black = [item[1] for item in bar_y]
    draw = [item[2] for item in bar_y]

    # Set position of bar on X axis
    br1 = np.arange(len(white))
    br2 = [x + barwidth for x in br1]
    br3 = [x + barwidth for x in br2]

    # Make the plot
    plt.bar(br1, white, width=barwidth,
            label='White')
    plt.bar(br2, black, width=barwidth,
            label='Black')
    plt.bar(br3, draw, width=barwidth,
            label='Draw')

    plt.xlabel('Episodes', fontweight='bold', fontsize=15)
    plt.ylabel('Stats', fontweight='bold', fontsize=15)
    plt.xticks([r + barwidth for r in range(len(white))],
               bar_x)

    plt.grid()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
