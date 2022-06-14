from Maze_class import Maze
from tqdm.auto import tqdm
from random import choice
import math
from abc import ABC, abstractmethod
from collections import defaultdict
import numpy as np


class MCTS:
    """Monte Carlo tree searcher. First rollout the tree then choose a move."""

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    def choose(self, node):
        """Choose the best successor of node. (Choose a move in the game)"""
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[str(node.step_history)], key=score)

    def do_rollout(self, node):  # Node is an agent state in a maze
        """Make the tree one layer better. (Train for one iteration.)"""
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        """Find an unexplored descendent of `node`"""
        path = []
        while True:
            path.append(node)
            if str(node.step_history) not in self.children or node.stuck:  # if the node itself is unexplored
                # the node's unique "name" is not in the tree's children or if the node is stuck
                return path
            unexplored = list(self.children.keys())
            unexplored.remove(str(node.step_history))
            if len(unexplored) > 0:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        """Update the `children` dict with the children of `node`"""
        if node is None:
            return
        if str(node.step_history) in self.children:
            return  # already expanded
        node.maze.update_explored(node.current_position)  # Update visited cell
        node.step(node.current_position, True)  # Update agent steps
        nodeee = node.find_children()
        self.children[str(node.step_history)] = nodeee

    def _simulate(self, node):
        """Returns the reward for a random simulation (to completion) of `node`"""
        while True:
            if node.finished or node.stuck:
                return node.reward()
            node = node.find_random_child()  # node.find_children()

    def _backpropagate(self, path, reward):
        """Send the reward back up to the ancestors of the leaf"""
        for node in reversed(path):
            self.N[str(node.step_history)] += 1
            self.Q[str(node.step_history)] += reward

    def _uct_select(self, node):
        """Select a child of node, balancing exploration & exploitation"""

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[str(node.step_history)])

        log_N_vertex = math.log(self.N[str(node.step_history)])

        def uct(n):
            """Upper confidence bound for trees"""
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[str(node.step_history)], key=uct)


class Node(ABC):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """

    @abstractmethod
    def find_children(self):
        """All possible successors of this board state"""
        return set()

    @abstractmethod
    def find_random_child(self):
        """Random successor of this board state (for more efficient simulation)"""
        return None

    @abstractmethod
    def is_terminal(self):
        """Returns True if the node has no children"""
        return True

    @abstractmethod
    def reward(self):
        """Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"""
        return 0

    @abstractmethod
    def __hash__(self):
        """Nodes must be hashable"""
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        """Nodes must be comparable"""
        return True


def start_a_maze(maze_size):
    return AgentInMaze(maze=Maze(maze_size, wall_value='W', corridor_value=' ', visited_value='v',
                                 agent_value='A', entrance_exit_value=9),
                       finished=False, stuck=False, step_history=[], current_position=None)


class AgentInMaze:
    def __init__(self, maze, finished, stuck, step_history, current_position):
        self.maze = maze
        self.finished = finished
        self.stuck = stuck
        if current_position is None:
            self.current_position = self.maze.entrance
        else:
            self.current_position = current_position
        self.step_history = step_history

    def find_children(self):
        if self.stuck:  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        possible_directions = {'up': None, 'down': None, 'left': None, 'right': None}
        current_position = self.current_position
        for step_direction in possible_directions:
            new_position = self.get_a_step(step_direction, current_position)
            if self.maze.in_maze(new_position):
                possible_directions[step_direction] = self.make_move(current_position, new_position)
            else:
                possible_directions[step_direction] = AgentInMaze(maze=self.maze, finished=False, stuck=True,
                                                                  step_history=self.step_history,
                                                                  current_position=new_position)

        return set(possible_directions.values())

    def find_random_child(self):
        if self.stuck:
            return self  # If the game is finished then no moves can be made
        possible_directions = {'up': None, 'down': None, 'left': None, 'right': None}
        empty_spots = []
        for direction in possible_directions:
            new_position = self.get_a_step(direction, self.current_position)
            if self.maze.in_maze(new_position):
                if self.maze.get_value(new_position) is self.maze.corridor_value:
                    empty_spots.append(new_position)

        empty_spots += self.maze.get_value_location(self.maze.visited_value)
        return self.make_move(self.current_position, choice(empty_spots))

    def reward(self):
        if self.finished:
            return 0
        else:
            return self.calc_distance_to_exit()

    def is_terminal(self):
        return self.stuck

    def get_a_step(self, step, current_position):
        if step == 'up':
            new_position = (current_position[0], current_position[1] + 1)
        if step == 'down':
            new_position = (current_position[0], current_position[1] - 1)
        if step == 'left':
            new_position = (current_position[0] - 1, current_position[1])
        if step == 'right':
            new_position = (current_position[0] + 1, current_position[1])

        return new_position

    def make_move(self, current_position, new_position):
        finished = self.is_finished(new_position)

        if finished:
            stuck = False
        else:
            stuck = self.is_stuck(self.maze.maze, new_position)

        # If it's possible to move in the new direction of if the new position is the exit cell.
        if self.maze.get_value(new_position) == self.maze.corridor_value or new_position == self.maze.exit:
            new_state = self.maze
            new_state.maze[new_position[0]][new_position[1]] = self.maze.agent_value

        else:
            new_state = self.maze

        print(f'\nCurrent position: {current_position}, new position: {new_position}, is stuck: {stuck}, '
              f'has finished: {finished}')
        print(f'Agent path: {self.step_history}')
        print(f'{self.maze.maze}\n')

        return AgentInMaze(maze=new_state, finished=finished, stuck=stuck,
                           step_history=self.step_history, current_position=new_position)

    def to_pretty_string(self):
        return f'\nCurrent state: \n{self.maze.maze}\n'

    def is_stuck(self, environment, new_position):
        destination = environment.loc[new_position[0]][new_position[1]]
        good_options = [self.maze.corridor_value, -self.maze.entrance_exit_value]
        if destination not in good_options:
            return True
        else:
            return False

    def is_finished(self, new_position):
        return new_position == self.maze.exit

    def step(self, new_position, make_a_step):
        self.step_history.append(self.current_position)
        if make_a_step:
            self.current_position = new_position

    def calc_distance_to_exit(self):
        current_position = np.array(self.current_position)
        exit_position = np.array(self.maze.exit)
        return math.sqrt(sum((current_position - exit_position)**2))


def find_path():
    tree = MCTS()
    bad_input = True
    while bad_input:
        maze_rows = 4  # input("Please enter the number of rows in the maze (int): ")
        maze_cols = 4  # input("Please enter the number of columbs in the maze (int): ")
        try:
            maze_size = (int(maze_rows), int(maze_cols))
            bad_input = False

        except ValueError:
            bad_input = True

    agent_state = start_a_maze(maze_size)
    print(agent_state.to_pretty_string())

    while True:
        for _ in tqdm(range(50)):
            tree.do_rollout(agent_state)
        agent_state = tree.choose(agent_state)
        print(agent_state.to_pretty_string())
        if agent_state.stuck:
            break


if __name__ == "__main__":
    find_path()
