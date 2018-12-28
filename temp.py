
import numpy as np


class Student:
    name = 'Udesh'
    age = '26'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print(self):
        print(self.name, self.age)



"""
a = Student('ude', 22)
b = Student('rav', 22)
c = Student('ravinga', 22)
s = Student('udesh', 22)
d = np.empty(shape=0, dtype=Student)
d = np.append(d, a)
d = np.append(d, b)
d = np.append(d, c)
d = np.append(d, s)
print(d.size)
d[0].print();
d = np.delete(d, 0)
print(d.size)
d[0].print(); """

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def get_index(phase, roads, step=5):
    index = int(phase * (step ** len(roads)))
    print(index)
    for rd in range(0, len(roads)):
        index += int((roads[rd] * (step ** (len(roads)-rd-1))))
        print(index, rd)
    return index

def real_val(phase, arr):
    print("func ", get_index(phase, arr))
    return phase*(5**4) + arr[0]*(5**3) + arr[1]*(5**2) + arr[2]*(5**1) + arr[3]


print(real_val(0,[1,2,3,4]))

if self.iter < 100:
    self.moving_vehi = 0
    self.moving_wait = 0
    self.moving_vehicle.append(vehicles)
    self.moving_wait_time.append(wait_time)
    for j in range(self.iter):
        self.moving_vehi += self.moving_vehicle[j]
        self.moving_wait += self.moving_wait_time[j]
    moving_avg = self.moving_wait / max(self.moving_vehi, 1)
else:
    out_vehi = self.moving_vehicle.popleft()
    out_wait = self.moving_wait_time.popleft()
    self.moving_vehicle.append(vehicles)
    self.moving_wait_time.append(wait_time)
    self.moving_vehi += vehicles - out_vehi
    self.moving_wait += wait_time - out_wait

    moving_avg = self.moving_wait / self.moving_vehi