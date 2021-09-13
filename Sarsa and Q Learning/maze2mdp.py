from mdpstate import MDPState
from copy import deepcopy

def maze_to_mdp(maze):

    """Returns a matrix of MDPState objects for each free space in a maze"""

    grid = deepcopy(maze)

    for i in range(1, len(maze) - 1):
        for j in range(1, len(maze[i]) - 1):

            #represent walls as #
            if maze[i][j] == '#':
                grid[i][j] = '#'
                continue

            if maze[i-1][j] == '#':
                north = (i, j)
            else:
                north = (i-1, j)

            if maze[i+1][j] == '#':
                south = (i, j)
            else:
                south = (i+1, j)

            if maze[i][j+1] == '#':
                east = (i, j)
            else:
                east = (i, j+1)

            if maze[i][j-1] == '#':
                west = (i, j)
            else:
                west = (i, j-1)

            grid[i][j] = MDPState(north, south, west, east)

    grid[1][1].reward = 10

    return(grid)
