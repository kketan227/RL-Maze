'''
The main file consisting of the code which imports other classes/files
'''

# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] < 3:
    raise Exception("Please use Python 3 because I used UTF coding")

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tqdm import tqdm
from sty import fg, bg, ef, rs

print (bg.blue + 'This has a blue background!' + bg.rs)

import random
import maze
import maze2mdp


size = 6
test = (maze.Maze(size,size))
print (test)
test_mdp = maze2mdp.maze_to_mdp(test.matrix)
# print (test_mdp)

# print (test_mdp [2][2])
# print (test_mdp [2][3])
# print (test_mdp [2][4])
# print (test_mdp [2][5])
# print (test_mdp [2][6])
# print (test_mdp [2][7])
# exit()
#
# world height
WORLD_HEIGHT = 2*size

# world width
WORLD_WIDTH = 2*size

# probability for exploration
EPSILON = 0.1

# step size
ALPHA = 0.5

# gamma for Q-Learning and Expected Sarsa
GAMMA = 1

# all possible actions
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

# initial state action pair values
START = [2*size-1, 2*size-1]
GOAL = [1, 1]

def step(state, action):
    i, j = state
    reward = -1

    if action == ACTION_UP:
        if(test_mdp[i-1][j]) == '#':
            reward = -25
            next_state = [i,j]
        next_state = [max(i - 1, 1), j]
    elif action == ACTION_LEFT:
        if(test_mdp[i][j-1]) == '#':
            reward = -25
            next_state = [i,j]
        next_state = [i, max(j - 1, 1)]
    elif action == ACTION_RIGHT:
        if(test_mdp[i][j+1]) == '#':
            reward = -25
            next_state = [i,j]
        next_state = [i, min(j + 1, WORLD_WIDTH - 1)]
    elif action == ACTION_DOWN:
        if(test_mdp[i+1][j]) == '#':
            reward = -25
            next_state = [i,j]
        next_state = [min(i + 1, WORLD_HEIGHT - 1), j]
    else:
        assert False

    # if (action == ACTION_DOWN and i == 2 and 1 <= j <= 10) or (
    #     action == ACTION_RIGHT and state == START):
    #     reward = -100
    #     next_state = START

    return next_state, reward


# choose an action based on epsilon greedy algorithm
def choose_action(state, q_value):
    if np.random.binomial(1, EPSILON) == 1:
        return np.random.choice(ACTIONS)
    else:
        values_ = q_value[state[0], state[1], :]
        return np.random.choice([action_ for action_, value_ in enumerate(values_) if value_ == np.max(values_)])


# an episode with Sarsa
# @q_value: values for state action pair, will be updated
# @return: total rewards within this episode
def sarsa(q_value):
    state = START
    # print(state)
    # print("upar state ye value")
    # print(q_value)
    action = choose_action(state, q_value)
    rewards = 0.0
    numberofsteps = 0
    while state != GOAL:
        next_state, reward = step(state, action)
        next_action = choose_action(next_state, q_value)
        rewards += reward

        target = q_value[next_state[0], next_state[1], next_action]

        #target *= GAMMA
        q_value[state[0], state[1], action] += ALPHA * (
                reward + q_value[next_state[0], next_state[1], next_action] - q_value[state[0], state[1], action])
        state = next_state
        action = next_action
        numberofsteps += 1
    # return rewards, numberofsteps
    arr=[]
    arr.append(rewards)
    arr.append(numberofsteps)
    return arr

# an episode with Q-Learning
# @q_value: values for state action pair, will be updated
# @step_size: step size for updating
# @return: total rewards within this episode
def q_learning(q_value, step_size=ALPHA):
    state = START
    rewards = 0.0
    numberofsteps = 0
    while state != GOAL:
        action = choose_action(state, q_value)
        next_state, reward = step(state, action)
        rewards += reward
        # Q-Learning update
        q_value[state[0], state[1], action] += step_size * (
                reward + GAMMA * np.max(q_value[next_state[0], next_state[1], :]) -
                q_value[state[0], state[1], action])
        state = next_state
        numberofsteps+=1
    #return rewards, numberofsteps
    arr=[]
    arr.append(rewards)
    arr.append(numberofsteps)
    return arr

# print optimal policy
def print_optimal_policy(q_value):
    optimal_policy = []
    for i in range(0, WORLD_HEIGHT):
        optimal_policy.append([])
        for j in range(0, WORLD_WIDTH):
            if [i, j] == GOAL:
                optimal_policy[-1].append('G')
                continue
            if [i, j] == START:
                optimal_policy[-1].append('S')
                continue

            if test_mdp [i][j] == "#":
                optimal_policy[-1].append('#')
                continue

            bestAction = np.argmax(q_value[i, j, :])
            if bestAction == ACTION_UP:
                optimal_policy[-1].append('↑')
            elif bestAction == ACTION_DOWN:
                optimal_policy[-1].append('↓')
            elif bestAction == ACTION_LEFT:
                optimal_policy[-1].append('←')
            elif bestAction == ACTION_RIGHT:
                optimal_policy[-1].append('→')
    for row in optimal_policy:
        print(row)
    for row in optimal_policy:
        print(row)
        break

# Use multiple runs instead of a single run and a sliding window
# With a single run I failed to present a smooth curve
# However the optimal policy converges well with a single run
# Sarsa converges to the safe path, while Q-Learning converges to the optimal path
def simulate():
    # episodes of each run
    episodes = 4500

    # perform 40 independent runs
    runs = 50

    rewards_sarsa = np.zeros(episodes)
    rewards_q_learning = np.zeros(episodes)
    numsteps_sarsa = np.zeros(episodes)
    numsteps_ql = np.zeros(episodes)
    for r in tqdm(range(runs)):
        q_sarsa = np.zeros((WORLD_HEIGHT, WORLD_WIDTH, 4))
        q_q_learning = np.copy(q_sarsa)
        for i in range(0, episodes):
            # cut off the value by -100 to draw the figure more elegantly
            # rewards_sarsa[i] += max(sarsa(q_sarsa), -100)
            # rewards_q_learning[i] += max(q_learning(q_q_learning), -100)
            # rewards_sarsa[i] += sarsa(q_sarsa)[0]
            # rewards_q_learning[i] += q_learning(q_q_learning)[0]
            sarsa_ret=sarsa(q_sarsa)
            ql_ret=q_learning(q_q_learning)
            rewards_sarsa[i] += sarsa_ret[0]
            rewards_q_learning[i] += ql_ret[0]
            numsteps_sarsa[i] += (sarsa_ret[1])
            numsteps_ql[i] += ql_ret[1]


    # averaging over independt runs
    rewards_sarsa /= runs
    rewards_q_learning /= runs

    numsteps_sarsa /= runs
    numsteps_ql /= runs

    # draw reward curves
    plt.plot(rewards_sarsa, label='Sarsa')
    plt.plot(rewards_q_learning, label='Q-Learning')
    plt.xlabel('Episodes')
    plt.ylabel('Sum of rewards during episode')
    #plt.ylim([-100, 0])
    plt.legend()
    stri =  'Number of runs = '+str(runs)
    plt.title(stri)
    #plt.figtext(0.8, 0.01, stri, wrap=True, horizontalalignment='center', fontsize=11)

    plt.savefig('rewards.png')
    plt.close()

    # draw steps curves
    plt.plot(numsteps_sarsa, label='Sarsa')
    plt.plot(numsteps_ql, label='Q-Learning')
    plt.xlabel('Episodes')
    plt.ylabel('num of steps')
    #plt.ylim([-100, 0])
    plt.title(stri)
    plt.legend()

    plt.savefig('steps.png')
    plt.close()


    # display optimal policy
    print('Sarsa Optimal Policy:')
    print_optimal_policy(q_sarsa)
    print('Q-Learning Optimal Policy:')
    print_optimal_policy(q_q_learning)


if __name__ == '__main__':
    simulate()
