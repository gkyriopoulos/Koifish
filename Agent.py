import json
import os
import random
import numpy
import FEN_encoder

import Engine


# Define the Q-learning agent
class QLearningAgent:
    def __init__(self):
        self.state_num = 116280
        self.action_num = 17 * 2

        # self.state_num = 27907200
        # self.action_num = 40

        self.file_name = "RKvsRK.json"
        self.actions = None
        self.learning_rate = 0.5
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_values = self.load_q()

    def get_q_value(self, state, action):
        if (state, action) not in self.q_values:
            self.q_values[(state, action)] = 0.0
        return self.q_values[(state, action)]

    def update_q_value(self, state, action, reward, next_state):
        current_q = self.get_q_value(state, action)
        max_q = max(self.get_q_value(next_state, a) for a in self.actions)
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_q - current_q)
        self.q_values[(state, action)] = new_q

    def choose_action(self, state):
        if self.actions:
            if random.random() < self.epsilon:
                return random.choice(self.actions)
            else:
                return max(self.actions, key=lambda a: self.get_q_value(state, a))

    def init_q(self):
        matrix = numpy.zeros((self.action_num, self.state_num))
        numpy.savetxt(self.file_name, matrix, delimiter=",")
        return

    def save_q(self):
        converted_data = {}
        converted_data = {str(key): value for key, value in self.q_values.items()}

        with open(self.file_name, "w") as file:
            json.dump(converted_data, file)

    def load_q(self):
        loaded_data = {}
        if os.path.exists(self.file_name):
            # Open the JSON file in read mode
            with open(self.file_name, 'r') as f:
                loaded_str_data = json.load(f)
            # Convert string keys back to tuples
            loaded_data = {eval(key): value for key, value in loaded_str_data.items()}
            return loaded_data
        else:
            return loaded_data

def train_agent(board_choice, num_episodes):
    # Q-learning training loop
    b_wins = 0
    w_wins = 0
    draws = 0

    for episode in range(num_episodes):
        my_engine = Engine.Engine(board_choice)
        current_state = FEN_encoder.encode_microchess_fen(my_engine.board)
        agent = QLearningAgent()
        chosen_action = None
        reward = None
        next_state = None
        old_state = None
        while my_engine.winner == "None":
            if my_engine.turn_player == "b":
                # print(my_engine.board)
                # Choose an action based on the current state
                agent.actions = my_engine.legal_moves.copy()
                chosen_action = agent.choose_action(current_state)
                # Perform the chosen action and observe the next state and reward
                next_state, reward = my_engine.attempt_move(chosen_action[0], chosen_action[1], "b")

                # print("Reward:", reward)

                next_state = FEN_encoder.encode_microchess_fen(next_state)

                # Update the Q-value for the current state-action pair
                agent.update_q_value(current_state, chosen_action, reward, next_state)

                old_state = current_state
                current_state = next_state
            else:
                random_move = random.choice(my_engine.legal_moves)
                my_engine.attempt_move(random_move[0], random_move[1], "w")
        if my_engine.winner == "b":
            b_wins += 1
        elif my_engine.winner == "w":
            agent.update_q_value(old_state, chosen_action, -100, next_state)
            w_wins += 1
        else:
            draws += 1

        print("Test Done:", my_engine.winner, "Game: ", episode, "Total stats: ", w_wins, "/", b_wins, "/", draws)
        agent.save_q()
