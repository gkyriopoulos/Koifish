import random
import numpy
import Utils
import Engine


# Define the Q-learning agent
class QLearningAgent:
    def __init__(self, filename, color):

        self.path = "train_data/"
        self.file_name = self.path + filename + "_" + color + ".json"
        self.actions = None
        self.learning_rate = 0.5
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_values = Utils.load_q(self)

    def get_q_value(self, state, action):
        key = "('{}', {})".format(state, action)
        if key not in self.q_values:
            self.q_values[key] = 0.0
        return self.q_values[key]

    def update_q_value(self, state, action, reward, next_state):
        key = "('{}', {})".format(state, action)
        current_q = self.get_q_value(state, action)
        if self.actions:
            max_q = max(self.get_q_value(next_state, a) for a in self.actions)
        else:
            max_q = 0
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_q - current_q)
        self.q_values[key] = new_q

    def choose_action(self, state):
        if self.actions:
            if random.random() < self.epsilon:
                return random.choice(self.actions)
            else:
                return max(self.actions, key=lambda a: self.get_q_value(state, a))


def train_agent_vs_random(board_choice, num_episodes, agent_color):
    # Q-learning training loop
    b_wins = 0
    w_wins = 0
    draws = 0
    rewards = numpy.zeros(num_episodes)

    agent = QLearningAgent(board_choice, agent_color)

    random_color = "b" if agent_color == "w" else "w"

    for episode in range(num_episodes):
        my_engine = Engine.Engine(board_choice)
        current_state = None
        chosen_action = None
        old_state = None
        reward_until_end = 0
        total_reward = 0
        while my_engine.winner == "None":
            if my_engine.turn_player == agent_color:
                current_state = Utils.encode_microchess_fen(my_engine.board)
                # Choose an action based on the current state
                agent.actions = my_engine.legal_moves.copy()
                chosen_action = agent.choose_action(current_state)
                # Perform the chosen action and observe the next state and reward
                next_state = my_engine.attempt_move(chosen_action[0], chosen_action[1], agent_color)[0]

                next_state = Utils.encode_microchess_fen(next_state)

                old_state = current_state
                current_state = next_state
            else:
                random_move = random.choice(my_engine.legal_moves)
                next_state = my_engine.attempt_move(random_move[0], random_move[1], random_color)[0]
                next_state = Utils.encode_microchess_fen(next_state)
                agent.actions = my_engine.legal_moves

                # if my_engine.legal_moves:
                # Update the Q-value for the current state-action pair
                if my_engine.moves > 1:
                    agent.update_q_value(old_state, chosen_action, 0, next_state)

                # old_state = current_state
                # current_state = next_state

        if my_engine.winner == "b":
            if agent_color == "b":
                total_reward = reward_until_end + 1
                agent.update_q_value(old_state, chosen_action, 1, current_state)
            else:
                total_reward = reward_until_end - 1
                agent.update_q_value(old_state, chosen_action, -1, current_state)
            b_wins += 1
        elif my_engine.winner == "w":
            if agent_color == "b":
                total_reward = reward_until_end - 1
                agent.update_q_value(old_state, chosen_action, -1, current_state)
            else:
                total_reward = reward_until_end + 1
                agent.update_q_value(old_state, chosen_action, 1, current_state)
            w_wins += 1
        else:
            # if reward > 0:
            #     total_reward = reward_until_end - 50
            #     agent.update_q_value(old_state, chosen_action, -50, current_state)
            # if reward < 0:
            #     total_reward = reward_until_end + 50
            #     agent.update_q_value(old_state, chosen_action, 50, current_state)
            # if reward == 0:
            #     agent.update_q_value(old_state, chosen_action, 0, current_state)
            draws += 1

        print("|Percentage: {:<5.3f}%   |Winner: {:<5}  |Game: {:<5}    |Total stats: {}/{}/{}|".format(
            round((episode + 1) / num_episodes * 100, 3), my_engine.winner, episode + 1, w_wins, b_wins, draws))
        rewards[episode] = total_reward
    Utils.save_q(agent)
    print("Q values for Agent successfully stored!")
    return numpy.cumsum(rewards)/num_episodes, (w_wins, b_wins, draws)

# TODO: EINAI LATHOS THELEI ALLAGES GIA NA PAIZEI SWSTA MIKRE ;)
# def train_agent_vs_agent(board_choice, num_episodes):
#     # Q-learning training loop
#
#     old_state_agent_1 = None
#     chosen_action_agent_1 = None
#     current_state_agent_1 = None
#     old_state_agent_2 = None
#     chosen_action_agent_2 = None
#     current_state_agent_2 = None
#     reward_agent_1 = None
#
#     b_wins = 0
#     w_wins = 0
#     draws = 0
#
#     agent_1_color = "b"
#     agent_2_color = "w"
#
#     agent1 = QLearningAgent(board_choice, agent_1_color)
#     agent2 = QLearningAgent(board_choice, agent_2_color)
#
#     for episode in range(num_episodes):
#         my_engine = Engine.Engine(board_choice)
#
#         while my_engine.winner == "None":
#             if my_engine.turn_player == agent_1_color:
#                 current_state_agent_1 = Utils.encode_microchess_fen(my_engine.board)
#                 # print(my_engine.board)
#                 # Choose an action based on the current state
#                 agent1.actions = my_engine.legal_moves.copy()
#                 chosen_action_agent_1 = agent1.choose_action(current_state_agent_1)
#                 # Perform the chosen action and observe the next state and reward
#                 next_state_agent_1, score_agent_1 = \
#                     my_engine.attempt_move(chosen_action_agent_1[0], chosen_action_agent_1[1], agent_1_color)
#
#                 # print("Reward:", reward)
#                 # if score_agent_1 < 0:
#                 #     reward_agent_1 = abs(score_agent_1)
#                 # else:
#                 #     reward_agent_1 = -abs(score_agent_1)
#
#                 next_state_agent_1 = Utils.encode_microchess_fen(next_state_agent_1)
#
#                 old_state_agent_1 = current_state_agent_1
#                 current_state_agent_1 = next_state_agent_1
#
#                 # Update the Q-value for the current state-action pair
#                 # agent1.update_q_value(old_state_agent_1, chosen_action_agent_1, reward_agent_1, next_state_agent_1)
#             else:
#                 current_state_agent_2 = Utils.encode_microchess_fen(my_engine.board)
#                 # print(my_engine.board)
#                 # Choose an action based on the current state
#                 agent2.actions = my_engine.legal_moves.copy()
#                 chosen_action_agent_2 = agent2.choose_action(current_state_agent_2)
#                 # Perform the chosen action and observe the next state and reward
#                 next_state_agent_2, score_agent_2 = \
#                     my_engine.attempt_move(chosen_action_agent_2[0], chosen_action_agent_2[1], agent_2_color)
#
#                 # print("Reward:", reward)
#                 # if score_agent_2 < 0:
#                 #     reward_agent_2 = -abs(score_agent_2)
#                 # else:
#                 #     reward_agent_2 = abs(score_agent_2)
#
#                 next_state_agent_2 = Utils.encode_microchess_fen(next_state_agent_2)
#
#                 old_state_agent_2 = current_state_agent_2
#                 current_state_agent_2 = next_state_agent_2
#
#                 # Update the Q-value for the current state-action pair
#                 # agent2.update_q_value(old_state_agent_2, chosen_action_agent_2, reward_agent_2, next_state_agent_2)
#         if my_engine.winner == "b":
#             agent1.update_q_value(old_state_agent_1, chosen_action_agent_1, 1, current_state_agent_1)
#             agent2.update_q_value(old_state_agent_2, chosen_action_agent_2, -1, current_state_agent_2)
#             b_wins += 1
#         elif my_engine.winner == "w":
#             agent1.update_q_value(old_state_agent_1, chosen_action_agent_1, -1, current_state_agent_1)
#             agent2.update_q_value(old_state_agent_2, chosen_action_agent_2, 1, current_state_agent_2)
#             w_wins += 1
#         else:
#             # if reward_agent_1 > 0:
#             #     agent1.update_q_value(old_state_agent_1, chosen_action_agent_1, -50, current_state_agent_1)
#             #     agent2.update_q_value(old_state_agent_2, chosen_action_agent_2, 50, current_state_agent_2)
#             # if reward_agent_1 < 0:
#             #     agent1.update_q_value(old_state_agent_1, chosen_action_agent_1, 50, current_state_agent_1)
#             #     agent2.update_q_value(old_state_agent_2, chosen_action_agent_2, -50, current_state_agent_2)
#             # if reward_agent_1 == 0:
#             #     agent1.update_q_value(old_state_agent_1, chosen_action_agent_1, 0, current_state_agent_1)
#             #     agent2.update_q_value(old_state_agent_2, chosen_action_agent_2, 0, current_state_agent_2)
#             draws += 1
#
#         print("|Percentage: {:<5.3f}%   |Winner: {:<5}  |Game: {:<5}    |Total stats: {}/{}/{}".format(
#             round((episode + 1) / num_episodes * 100, 3), my_engine.winner, episode + 1, w_wins, b_wins, draws))
#     Utils.save_q(agent1)
#     print("Q values for Agent1 successfully stored!")
#     Utils.save_q(agent2)
#     print("Q values for Agent2 successfully stored!")
