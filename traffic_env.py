import numpy as np
from display import Display
TIME_STEP = 10
DEBUG = 1
from collections import deque

def info(level, a):
    if DEBUG < level:
        print(a)


class VehicleBlock:

    def __init__(self, num_vehicles):
        self.num_vehicles = num_vehicles
        self.current_time = 0

    def step(self, time_step):
        self.current_time += time_step
        return self.current_time

    def waiting_time(self):
        # if DEBUG:
        #    print("Vehicle block: ", self.num_vehicles, self.current_time)
        return self.num_vehicles * self.current_time

    def reduce_vehicles(self, num_vehicles):
        self.num_vehicles -= num_vehicles

    def get_num_vehicles(self):
        return self.num_vehicles


class Road:

    def __init__(self, rid):  # road id
        self.list = np.empty(shape=0, dtype=VehicleBlock)
        self.id = rid

    def add_block(self, vb):
        if self.get_num_vehicles() + vb.get_num_vehicles() <= 40:
            self.list = np.append(self.list, vb)
            print(" Number of vehicles added : ", self.id, vb.get_num_vehicles())
        #else:
        #    self.list = np.append(self.list, VehicleBlock(40 - self.get_num_vehicles()))
        #    print(" Number of vehicles added (full) : ", self.id, 40 - self.get_num_vehicles())

    def remove_block(self):
        if self.list.size == 0:
            return 0, 0
        if self.list[0].get_num_vehicles() < 10:
            temp_a, temp_b = self.list[0].step(TIME_STEP) * self.list[0].get_num_vehicles(), self.list[0].get_num_vehicles()
            self.list = np.delete(self.list, 0)
            return temp_a, temp_b
        else:
            self.list[0].reduce_vehicles(10)
            return self.list[0].step(TIME_STEP) * 10, 10

    def get_wait_time(self):
        time = 0
        for i in range(0, self.list.size):
            time += self.list[i].waiting_time()
            #info(2, ' Road id : ' + str(self.id) + ' Wait time: ' + str(time))

        return time

    def get_num_vehicles(self):
        total = 0
        for i in range(0, self.list.size):
            total += self.list[i].get_num_vehicles()
        #info(2, 'Road id : ' + str(self.id) + ' Number of vehicles: ' + str(total))
        return total

    def step(self, time_step):
        for i in range(0, self.list.size):
            self.list[i].step(time_step)


class TrafficEnv:
    q_length_step_size = 6
    num_phases = 4
    num_roads = 4
    curr_waiting_time = 0
    curr_phase = 0
    dp = Display()

    def __init__(self, array):
        self.env = array
        self.road = np.array([Road(0), Road(1), Road(2), Road(3)])
        self.road[0].add_block(VehicleBlock(10))
        self.road[1].add_block(VehicleBlock(30))
        self.road[2].add_block(VehicleBlock(20))
        self.road[3].add_block(VehicleBlock(40))
        self.gap_indicator = 1
        self.wait_time = 0
        self.vehicles = 0
        self.iter = 0
        self.highest_wait_time = deque(maxlen=10)

    # step function advance the time in environment
    # When agent performs the action, step() method simulate
    # the environment

    def step(self, action, load):
        #  Pre reward calculations
        prev_wait_time = self.total_wait_time()
        pre_reward = max(self.road[0].get_num_vehicles(), self.road[1].get_num_vehicles(),
                         self.road[2].get_num_vehicles(), self.road[3].get_num_vehicles()) \
                    -min(                                   self.road[0].get_num_vehicles(),
                                                            self.road[1].get_num_vehicles(),
                                                            self.road[2].get_num_vehicles(),
                                                            self.road[3].get_num_vehicles())
        #  Pre reward calculations
        wait_time, vehicles = self.road[action].remove_block()
        self.wait_time += wait_time
        self.vehicles += vehicles

        self.highest_wait_time.append(wait_time/max(vehicles, 1))

        out_wait_highest = self.deque_highest_val(self.highest_wait_time)
        self.dp.figure_time(wait_time/max(vehicles, 1), self.iter, 4)

        if self.vehicles != 0:
            avg_wait_time = self.wait_time/self.vehicles

        self.dp.figure_time(self.vehicles, self.iter)
        self.dp.figure_time(avg_wait_time, self.iter, 2)
        self.iter += 1

        self.local_step(TIME_STEP)
        # update_env if needed : uniform distribution

        if self.gap_indicator % load == 0:
            self.update_env()
            print(" Env Updated")
        self.gap_indicator += 1
        # calculate reward achieved
        next_wait_time = self.total_wait_time()
        reward = max(self.road[0].get_num_vehicles(), self.road[1].get_num_vehicles(), self.road[2].get_num_vehicles(),
                     self.road[3].get_num_vehicles()) - min(self.road[0].get_num_vehicles(),
                                                            self.road[1].get_num_vehicles(),
                                                            self.road[2].get_num_vehicles(),
                                                            self.road[3].get_num_vehicles())

        if(prev_wait_time == 0) & (next_wait_time == 0):
            reward = 0
        else:
            reward = (prev_wait_time - next_wait_time)/max(prev_wait_time, next_wait_time)
        #reward = pre_reward - reward
        '''if self.gap_indicator != 1:
            if next_wait_time == 0:
                reward = 1
            else:
                reward = (prev_wait_time - next_wait_time)/max(prev_wait_time,next_wait_time )
        else:
            reward = 0
'''
        if DEBUG:
            print("Reward given : ", reward)
            print("Time : ", next_wait_time, prev_wait_time)

        self.curr_phase = action  # currently phase is same as action
        state_vector = []
        for i in range(0, 4):
            #print("ID and Wait time", i, self.road[i].get_wait_time())
            state_vector.append(min(4, int(self.road[i].get_wait_time()/200)))
            #state_vector.append(self.road[i].get_num_vehicles()/10)

        self.dp.plot(vehicle_data=state_vector)
        return self.curr_phase, state_vector, reward

    # Update the environment with some vehicles in
    # a random fashion

    def update_env(self):  # add vehicles to environment
        random_vehicles = np.array([np.random.poisson(4, 1)[0], np.random.poisson(2, 1)[0], np.random.poisson(1, 1)[0],
                          np.random.poisson(3, 1)[0]])  # poison distribution of vehicles in road network
        random_vehicles = random_vehicles.round()
        # random_vehicles = [1,2,1,2]
        np.clip(random_vehicles, 0, 4)

        for road_index in range(0, 4):
            self.road[road_index].add_block(VehicleBlock(int(random_vehicles[road_index]*10)))

    # Calculate total wait time of all roads at the intersection
    def total_wait_time(self):
        total_time = 0
        for i in range(0, self.num_roads):
            total_time += self.road[i].get_wait_time()
        return total_time

    # internal step function for each road with given time step
    def local_step(self, time_step):
        for i in range(0, self.num_roads):
            self.road[i].step(time_step)

    @staticmethod
    def deque_highest_val(dq):
        max_dq = 0
        for i in dq:
            if i > max_dq:
                max_dq = i
        return max_dq
