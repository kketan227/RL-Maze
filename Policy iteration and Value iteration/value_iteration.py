'''
Has the code for value iteration without any visualization to save the
    computation time.
'''

import maze
import maze2mdp
import AnimationFile as af
import turtle
from tabulate import tabulate


def value_iteration(grid, gamma):
    """
    Performs value iteration on a given grid of MDPState objects.
    """

    af.setup_maze(grid)

    policy = [['up' for i in range(len(grid[0]))] for j in range(len(grid))]
    actions = ['up', 'down', 'left', 'right']

    is_value_changed = True

    iterations = 0
    final_values=[]

    # iterate values until convergence
    while is_value_changed:
        is_value_changed = False
        biglist=[]
        for i in range(len(grid)):
                smalllist=[]
                for j in range(len(grid[i])):
                    if grid[i][j] != '#':
                        q = []
                        for a in actions:
                            neighbor = getattr(grid[i][j], a) # Get coordinates of neighboring cell
                            q.append(grid[i][j].reward + gamma * grid[neighbor[0]][neighbor[1]].value)
                        v = max(q)
                        smalllist.append(v)

                        if v != grid[i][j].value:
                            is_value_changed = True
                            grid[i][j].value = v
                    else:
                        smalllist.append('#')

                biglist.append(smalllist)

        # print(tabulate(biglist))  # To print the values of each state
        final_values=biglist

        #print("new Iteration")
        iterations += 1

    print(tabulate(final_values))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != '#':
                # Dictionary comprehension to get value associated with each action
                action_values = {a: grid[getattr(grid[i][j], a)[0]][getattr(grid[i][j], a)[1]].value for a in actions}
                # action_values gives the value of the square according to each action from top to bottom
                policy[i][j] = max(action_values, key=action_values.get)
                # This picks the best out for each of the grid's actions
                # Compare to previous policy
            else:
                policy[i][j] = '#'

    #print("Number of iterations taken "+str(iterations))
    return(policy)


if __name__ == '__main__':
    test_maze = maze.Maze(w=7, h=7)
    print((test_maze))
    test_mdp = maze2mdp.maze_to_mdp(test_maze.matrix)
    test_policy = value_iteration(test_mdp, .9)
    print(tabulate(test_policy))


    #print(test_maze)
    #print(test_policy_str)
