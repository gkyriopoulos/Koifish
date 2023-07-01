import numpy as np

# THIS ISNT THE ORIGINAL CLASS TO WORK WITH, ITS AN IMPLEMENTATION THAT HAS TO CHANGE TO OUR ENVIRONMENT

class Node():
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)

    def update(self, result):
        self.visits += 1
        self.wins += result

    def fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.wins / c.visits) + c_param * np.sqrt((2 * np.log(self.visits) / c.visits))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

class MCTS():
    def __init__(self, root, n_simulations):
        self.root = root
        self.n_simulations = n_simulations

    def search(self):
        for _ in range(self.n_simulations):
            v = self.tree_policy()
            reward = self.default_policy(v.state)
            self.backup(v, reward)

    def tree_policy(self):
        v = self.root
        while not v.state.is_terminal():
            if not v.fully_expanded():
                return self.expand(v)
            else:
                v = v.best_child()
        return v

    def expand(self, node):
        tried_children = [c.state for c in node.children]
        new_state = node.state.get_next_state()
        while new_state in tried_children:
            new_state = node.state.get_next_state()
        node.add_child(new_state)
        return node.children[-1]

    def default_policy(self, state):
        while not state.is_terminal():
            state = state.get_next_state()
        return state.get_reward()

    def backup(self, node, reward):
        while node is not None:
            node.update(reward)
            node = node.parent
