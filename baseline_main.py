"""Training the agent"""
import gym as env
import numpy as np
import random
from display import Display
from IPython.display import clear_output
from traffic_env import TrafficEnv
from collections import deque

# q_table = np.zeros([env.observation_space.n, env.action_space.n])

# implement a queue table here for a single intersection


def get_index(phase, roads, step=5):
    index = int(phase * (step ** len(roads)))
    for rd in range(0, len(roads)):
        index += int((roads[rd] * (step ** (len(roads)-rd-1))))
    return index



DEBUG = True

phases = 4
num_roads = 4
vehicle_step = 5
actions = phases
q_table = np.full((phases * (vehicle_step ** num_roads), actions), -0.75)
action = np.zeros(phases)

#  Parameters for Q function

alpha = 0.6  # TODO: tune parameters
gamma = 0.2  # TODO: tune parameters
epsilon = 0.1  # TODO: Change over the time

# For plotting metrics
all_epochs = []
all_penalties = []

# init vehicles at a intersection
array = np.zeros(shape=(1, num_roads))  # TODO: init array
array = [1, 3, 2, 4]
traffic_env = TrafficEnv(array)

# updating values
curr_phase = 0
curr_road_loads = np.zeros(shape=num_roads)
next_road_loads = np.zeros(shape=num_roads)
moving_avg = 0
moving_que = deque(maxlen=100)
dp = Display()
action = 1
for i in range(0, 15000):

    if i % 8 == 0:
        action += 1
        if action == 4:
            action = 0

    load = max(9, 10 - (int(i/100) % 10))
    if DEBUG:
        print("Action selected: " + str(action) + " at step " + str(i) + " Load " + str(load))



    # take decision on reward
    next_phase, next_road_loads, reward = traffic_env.step(action, load)

    old_value = q_table[get_index(curr_phase, curr_road_loads), action]
    next_max = np.max(q_table[get_index(next_phase, next_road_loads)])

    new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)  # calculate Q value
    q_table[get_index(curr_phase, curr_road_loads), action] = new_value
    curr_phase = next_phase
    curr_road_loads = next_road_loads

# moving average **** TODO: Declare a separate function
    if i < 100:
        moving_avg = 0
        moving_que.append(reward)
        for j in range(i):
            moving_avg += moving_que[j]
        moving_avg = moving_avg / (i + 1)
    else:
        out = moving_que.popleft()
        moving_que.append(reward)
        moving_avg += ((reward - out) / 100)

    dp.figure(moving_avg, i)
# moving average ****


dp.plot3d(q_table)

print("Q table", q_table)
print("Training finished.\n")
