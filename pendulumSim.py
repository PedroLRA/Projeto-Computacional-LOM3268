import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin

import matplotlib.animation as animation

import pandas as pd
from itertools import product
from tqdm import tqdm
from body import CreateBodyPen
from display import show


class PendulumSim():
    """
    Creates the simulation scene based on the following inputs:
        - body1: information of the first body
        - body2: information of the second body
        - G: Corresponds to the gravity value; when not provided, defaults to the value of the constant in the SI unit
            numerical value as int or float

    """
    def __init__(self, body1, body2, G = 9.8, origin = [0,0,0]):
        self.bodies = [body1, body2]
        #self.numOfBodies = len(self.bodies)

        self.G = G
        self.L1 = body1.length
        self.L2 = body2.length
        self.M1 = body1.mass
        self.M2 = body2.mass
        self.th1 = body1.theta
        self.w1 = body1.w
        self.th2 = body2.theta
        self.w2 = body2.w

        self.L = self.L1 + self.L2
        self.origin = origin


    def simulate(self, timeInterval, dt = 0.01):

    # create a time array from 0..t_stop sampled at 0.02 second steps
        self.dt = dt
        self.time = np.arange(timeInterval[0], timeInterval[1]+self.dt, self.dt)
        self.numIterations = len(self.time)
        # th1 and th2 are the initial angles (degrees)
        # w10 and w20 are the initial angular velocities (degrees per second)


        time_list = []

    # initial state
        state = np.radians([self.th1, self.w1, self.th2, self.w2])


    # integrate the ODE using Euler's method
        y = np.empty((len(self.time), 4))
        
        y[0] = state
        for i in range(1, len(self.time)):

            y[i] = y[i - 1] + self.derivs(self.time[i - 1], y[i - 1]) * dt
            time_list.append(self.time[i - 1])


        time_list.append(self.time[-1])

        time_array = np.array(time_list)

        x1 = self.L1*sin(y[:, 0])
        y1 = -self.L1*cos(y[:, 0])

        x2 = self.L2*sin(y[:, 2]) + x1
        y2 = -self.L2*cos(y[:, 2]) + y1

        body1 = [x1, y1]
        body2 = [x2, y2]
        self.body1_array = np.array(body1)
        self.body2_array = np.array(body2)


        #print('body1', body1)
        #print('body2', body2)
        #print('time array', time_array)

        
        
    
    def derivs(self, t, state):
        dydx = np.zeros_like(state)

        dydx[0] = state[1]

        delta = state[2] - state[0]
        den1 = (self.M1+self.M2) * self.L1 - self.M2 * self.L1 * cos(delta) * cos(delta)
        dydx[1] = ((self.M2 * self.L1 * state[1] * state[1] * sin(delta) * cos(delta)
                    +self.M2 * self.G * sin(state[2]) * cos(delta)
                    + self.M2 * self.L2 * state[3] * state[3] * sin(delta)
                    - (self.M1+self.M2) * self.G * sin(state[0]))
                / den1)

        dydx[2] = state[3]

        den2 = (self.L2/self.L1) * den1
        dydx[3] = ((- self.M2 * self.L2 * state[3] * state[3] * sin(delta) * cos(delta)
                    + (self.M1+self.M2) * self.G * sin(state[0]) * cos(delta)
                    - (self.M1+self.M2) * self.L1 * state[1] * state[1] * sin(delta)
                    - (self.M1+self.M2) * self.G * sin(state[2]))
                / den2)

        return dydx
    
    def showScene(self, dtStepPerFrame = 1, use_lines = False):
        """
        Utiliza a função externa show() para realizar o plot da animação da simulação

        Pode receber como entrada a seguinte variável:
            dtStepPerFrame: O valor que corresponderá à quantidade de passos que será pulada para cada frame da simulação
                int
        """
        self.positions = np.zeros([2, 3, self.numIterations])
        self.positions[0,:3:2, :] = self.body1_array
        self.positions[1,:3:2, :] = self.body2_array
        #print(self.positions)

        self.numOfBodies = 2
        


        show(self, dtStepPerFrame, use_lines)

    

if __name__ == "__main__":
    from body import CreateBodyPen
    import matplotlib.pyplot  as plt

    body1 = CreateBodyPen(1,0, 1, 120, 10)
    body2 = CreateBodyPen(1,0, 1, -10, 10)

    scene = PendulumSim(body1, body2)

    scene.simulate([0,10], dt = 0.01)
    #print(body1, body2, time_array)


    scene.showScene(dtStepPerFrame=1, use_lines=True)








