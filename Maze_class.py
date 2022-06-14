import pandas as pd
import random


class Maze:
    def __init__(self, size, wall_value, corridor_value, entrance_exit_value, agent_value, visited_value):
        self.cols = size[0]
        self.rows = size[1]
        self.maze = self.maze_generator(wall_value, corridor_value, entrance_exit_value)
        self.entrance = self.get_value_location(entrance_exit_value)[0]
        self.exit = self.get_value_location(-entrance_exit_value)[0]
        self.wall_value = wall_value
        self.corridor_value = corridor_value
        self.entrance_exit_value = entrance_exit_value
        self.agent_value = agent_value
        self.visited_value = visited_value

    def maze_generator(self, numerical_wall_value, numerical_corridor_value, numerical_entrance_exit_value):
        def surroundingCells(_rand_wall):
            _s_cells = 0
            if maze[_rand_wall[0] - 1][_rand_wall[1]] == 'c':
                _s_cells += 1
            if maze[_rand_wall[0] + 1][_rand_wall[1]] == 'c':
                _s_cells += 1
            if maze[_rand_wall[0]][_rand_wall[1] - 1] == 'c':
                _s_cells += 1
            if maze[_rand_wall[0]][_rand_wall[1] + 1] == 'c':
                _s_cells += 1

            return _s_cells

        height = self.rows
        width = self.cols
        cell = 'c'
        unvisited = 'u'
        maze = []

        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append(unvisited)
            maze.append(line)

        # Randomize starting point and set it a cell
        starting_height = int(random.random() * height)
        starting_width = int(random.random() * width)
        if starting_height == 0:
            starting_height += 1
        if starting_height == height - 1:
            starting_height -= 1
        if starting_width == 0:
            starting_width += 1
        if starting_width == width - 1:
            starting_width -= 1

        # Mark it as cell and add surrounding walls to the list
        maze[starting_height][starting_width] = cell
        walls = [[starting_height - 1, starting_width], [starting_height, starting_width - 1],
                 [starting_height, starting_width + 1], [starting_height + 1, starting_width]]

        # Denote walls in maze
        maze[starting_height - 1][starting_width] = 'w'
        maze[starting_height][starting_width - 1] = 'w'
        maze[starting_height][starting_width + 1] = 'w'
        maze[starting_height + 1][starting_width] = 'w'

        while walls:
            # Pick a random wall
            rand_wall = walls[int(random.random() * len(walls)) - 1]

            # Check if it is a left wall
            if rand_wall[1] != 0:
                if maze[rand_wall[0]][rand_wall[1] - 1] == 'u' and maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
                    # Find the number of surrounding cells
                    s_cells = surroundingCells(rand_wall)

                    if s_cells < 2:
                        # Denote the new path
                        maze[rand_wall[0]][rand_wall[1]] = 'c'

                        # Mark the new walls
                        # Upper cell
                        if rand_wall[0] != 0:
                            if maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                                maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Bottom cell
                        if rand_wall[0] != height - 1:
                            if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                                maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])

                        # Leftmost cell
                        if rand_wall[1] != 0:
                            if maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                                maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if rand_wall[0] != 0:
                if maze[rand_wall[0] - 1][rand_wall[1]] == 'u' and maze[rand_wall[0] + 1][rand_wall[1]] == 'c':

                    s_cells = surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        maze[rand_wall[0]][rand_wall[1]] = 'c'

                        # Mark the new walls
                        # Upper cell
                        if rand_wall[0] != 0:
                            if maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                                maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Leftmost cell
                        if rand_wall[1] != 0:
                            if maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                                maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                        # Rightmost cell
                        if rand_wall[1] != width - 1:
                            if maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                                maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check the bottom wall
            if rand_wall[0] != height - 1:
                if maze[rand_wall[0] + 1][rand_wall[1]] == 'u' and maze[rand_wall[0] - 1][rand_wall[1]] == 'c':

                    s_cells = surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        maze[rand_wall[0]][rand_wall[1]] = 'c'

                        # Mark the new walls
                        if rand_wall[0] != height - 1:
                            if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                                maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if rand_wall[1] != 0:
                            if maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                                maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])
                        if rand_wall[1] != width - 1:
                            if maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                                maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check the right wall
            if rand_wall[1] != width - 1:
                if maze[rand_wall[0]][rand_wall[1] + 1] == 'u' and maze[rand_wall[0]][rand_wall[1] - 1] == 'c':

                    s_cells = surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        maze[rand_wall[0]][rand_wall[1]] = 'c'

                        # Mark the new walls
                        if rand_wall[1] != width - 1:
                            if maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                                maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])
                        if rand_wall[0] != height - 1:
                            if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                                maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if rand_wall[0] != 0:
                            if maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                                maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Delete the wall from the list anyway
            for wall in walls:
                if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                    walls.remove(wall)

        # Mark the remaining unvisited cells as walls
        for i in range(0, height):
            for j in range(0, width):
                if maze[i][j] == 'u':
                    maze[i][j] = 'w'

        # Set entrance and exit
        for i in range(0, width):
            if maze[1][i] == 'c':
                maze[0][i] = 'en'
                break

        for i in range(width - 1, 0, -1):
            if maze[height - 2][i] == 'c':
                maze[height - 1][i] = 'ex'
                break

        numerical_maze = []
        for row in maze:
            numerical_row = []
            for cell in row:
                if cell == 'w':
                    numerical_row.append(numerical_wall_value)  # wall
                elif cell == 'en':
                    numerical_row.append(numerical_entrance_exit_value)
                elif cell == 'ex':
                    numerical_row.append(-numerical_entrance_exit_value)
                else:
                    numerical_row.append(numerical_corridor_value)  # corridor
            numerical_maze.append(numerical_row)

        return pd.DataFrame(numerical_maze)

    def get_value_location(self, value):
        relevant_cells = []
        for row in self.maze.index:
            for col in self.maze.columns:
                if self.maze[row][col] == value:
                    relevant_cells.append((row, col))

        return relevant_cells

    def update_explored(self, location):
        options = [self.corridor_value, self.agent_value, self.entrance_exit_value]
        if self.maze[location[0]][location[1]] in options:
            self.maze[location[0]][location[1]] = self.visited_value

    def in_maze(self, location):
        col = location[0]
        row = location[1]

        return col in self.maze.index and row in self.maze.columns

    def get_value(self, location):
        return self.maze[location[0]][location[1]]


# maze_size = (10, 10)
# a_maze = Maze(maze_size)
# print(a_maze.maze)
