'''
Actual code for policy iteration which has the animations showing the updates
    to a policy towards an optimal policy
'''

import turtle
import random
import maze
import maze2mdp
import AnimationFile
from tabulate import tabulate
from time import sleep

wn = turtle.Screen()
wn.bgcolor("White")
wn.title("A Maze Game")
wn.setup(700,700)
#wn.exitonclick()

def policy_iteration_animate(grid, gamma):
    is_policy_changed = True

    AnimationFile.setup_maze(grid)

    actions = ['up', 'down', 'left', 'right']

    #Initializing with all up in the below line
    policy = [['up' for i in range(len(grid[0]))] for j in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '#':
                policy[i][j] = '#'

    iterations = 0
    AnimationFile.animate_policy(policy, iterations)
    sleep(1)


    # Policy iteration
    while is_policy_changed:
        is_policy_changed = False
        #print(policy)
        # Policy evaluation
        # Transition probabilities not shown due to deterministic setting
        is_value_changed = True
        while is_value_changed:
            is_value_changed = False
            biglist=[]
            # Run value iteration for each state
            for i in range(len(grid)):
                smalllist=[]
                for j in range(len(grid[i])):
                    if grid[i][j] == '#':
                        policy[i][j] = '#'
                        smalllist.append('#')
                    else:
                        neighbor = getattr(grid[i][j], policy[i][j])
                        v = grid[i][j].reward + gamma * grid[neighbor[0]][neighbor[1]].value
                        smalllist.append(v)
                        # Compare to previous iteration
                        if v != grid[i][j].value:
                            is_value_changed = True
                            grid[i][j].value = v
                biglist.append(smalllist)
            #print(tabulate(biglist))

        # Once values have converged for the policy, update policy with greedy actions
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] != '#':
                    # Dictionary comprehension to get value associated with each action
                    action_values = {a: grid[getattr(grid[i][j], a)[0]][getattr(grid[i][j], a)[1]].value for a in actions}
                    best_action = max(action_values, key=action_values.get)
                    # Compare to previous policy
                    if best_action != policy[i][j]:
                        is_policy_changed = True
                        policy[i][j] = best_action

        iterations += 1
        AnimationFile.animate_policy(policy, iterations)


    sleep(3)
    turtle.bye()
    return(policy)

#Create class instances
pen = AnimationFile.Pen()

#Set up the maze
if __name__ == '__main__':
    random.seed(105)
    #test = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#'], ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#'], ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#'], ['#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', '#'], ['#', ' ', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#'], ['#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#'], ['#', ' ', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'], ['#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]
    test = (maze.Maze(8,8))
    print (test)
    test_mdp = maze2mdp.maze_to_mdp(test.matrix)
    test_policy = policy_iteration_animate(test_mdp, .9)
    print(tabulate(test_policy))
    #print(test_policy)
    #setup_maze(test_grid)
