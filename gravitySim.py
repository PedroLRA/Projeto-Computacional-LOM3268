import numpy as np
import pandas as pd
from itertools import product
from tqdm import tqdm
from body import CreateBodyGrav
from display import show

class GravitySim():
    """
    Creates the simulation scene based on the following inputs:
        - bodiesArray: Array of Body objects created from the CreateBody class
            [body1, body2, ...]
        - G: Corresponds to the gravitational constant; when not provided, defaults to the value of the constant in the SI unit
            numerical value as int or float

    """

    def __init__(self, bodiesArray, G = 6.674184):
        self.bodies = bodiesArray
        self.numOfBodies = len(self.bodies)
        
        self.G = G

    def simulate(self, timeInterval, dt = 1, method = 'verlet'):
        """
    Calculates all simulation intervals within a given time range.
    
    Takes the following variables as input:
        - timeInterval: A list containing the initial and final time for which the simulation will be conducted
            [initial_time, final_time]
        - dt: Time step to be used during the process
            numerical value as int or float
        - method: Corresponds to the method that will be used to calculate the positions of the bodies in the simulation; it can be one of the following:
            "verlet": performs calculations using the Verlet integration
            "eqMov": performs calculations using the equations of motion

        """

        self.dt = dt
        self.time = np.arange(timeInterval[0], timeInterval[1]+self.dt, self.dt)
        self.numIterations = len(self.time)
        
        #Initializes the creation of variables where all calculated values throughout the simulation will be stored.
        self.positions = np.zeros([self.numOfBodies, 3, self.numIterations])
        self.velocities = np.zeros([self.numOfBodies, 3, self.numIterations])
        self.accelerations = np.zeros([self.numOfBodies, 3, self.numIterations])
        self.masses = np.zeros((self.numOfBodies,1))

        #Assigning the initial conditions to the variables above
        for bodyIndex in range(self.numOfBodies):
            self.masses[bodyIndex,0] = self.bodies[bodyIndex].mass
            self.positions[bodyIndex, :, 0] = self.bodies[bodyIndex].position
            self.velocities[bodyIndex, :, 0] = self.bodies[bodyIndex].velocity

        #Loop to calculate the new positions, velocities and accelerations of bodies over the time interval        
        if method == 'verlet':
            self.iter = 1
            self.movementEq()
            for currentTime in tqdm(range(2,self.numIterations), desc="Simulating"):
                self.iter = currentTime
                self.verlet() 
        elif method == 'eqMov':
            for currentTime in tqdm(range(1,self.numIterations), desc="Simulating"):
                self.iter = currentTime
                self.movementEq()
    
    def movementEq(self):
        """ Calculates new positions from the equations of motion"""        
        forces = self.calculateForces()
        #Calculate and add new properties for each body        
        self.accelerations[:, :, self.iter] = forces[:] / self.masses[:]
        self.velocities[:, :, self.iter] = self.velocities[:, :, self.iter-1] + self.accelerations[:, :, self.iter] * self.dt
        self.positions[:, :, self.iter] = self.positions[:, :, self.iter-1] + self.velocities[:, :, self.iter-1] * self.dt + self.accelerations[:, :, self.iter] * self.dt**2 / 2

    def calculateForces(self):
        """ Calculate the forces exerted between bodies"""

        bodiesIndexes = range(self.numOfBodies)
        bodyInteractions = list(product(bodiesIndexes,bodiesIndexes)) #lista com todas as interações entre corpos
        
        forcesMatrix = np.zeros((self.numOfBodies,self.numOfBodies,3)) #matriz de forças (corpo_i, corpo_j, coordenada)

        for interaction in bodyInteractions:
            i, j = interaction
            
            if i < j:
                r = self.positions[j, :, self.iter-1] - self.positions[i, :, self.iter-1] #Vetor distância
                rNorm = np.linalg.norm(r)  #Norma do vetor distância

                force = -self.G * self.masses[i,0] * self.masses[j,0] / rNorm**2 * r/rNorm #Força entre os cors i e j

                forcesMatrix[i,j,:] = -force
                forcesMatrix[j,i,:] = force

        return np.sum(forcesMatrix, axis=1) #retorna um array com as forças resultantes

    def verlet(self):
        """ Calculate new positions using the verlet integration method"""
        forces = self.calculateForces()

        #Calculates and adds new properties for each body
        self.accelerations[:, :, self.iter] = forces[:] / self.masses[:]
        self.positions[:, :, self.iter] = self.accelerations[:, :, self.iter] * self.dt**2 - self.positions[:, :, self.iter-2] + 2 * self.positions[:, :, self.iter-1]
        self.velocities[:, :, self.iter] = self.velocities[:, :, self.iter] + self.accelerations[:, :, self.iter] * self.dt

    def showScene(self, dtStepPerFrame = 1):
        """
        Uses the external show() function to plot the simulation animation

         It can receive the following variable as input:
             dtStepPerFrame: The value that will correspond to the number of steps that will be skipped for each frame of the simulation
                 int
        """
        show(self, dtStepPerFrame)

    def exportDF(self):
        """ Export all calculated data in the format of a pandas dataframe"""
        dfDict = {}

        dfDict['time'] = self.time

        for bodyIndex in range(self.numOfBodies):
            dfDict[f'body-{bodyIndex} X position'] = self.positions[bodyIndex, 0, :]
            dfDict[f'body-{bodyIndex} Y position'] = self.positions[bodyIndex, 1, :]
            dfDict[f'body-{bodyIndex} Z position'] = self.positions[bodyIndex, 2, :]

        return pd.DataFrame(dfDict)

if __name__ == "__main__":
    from body import CreateBodyGrav

    sol = CreateBodyGrav(333000,position_vector=[0,0,0],velocity_vector=[0,0,0],acceleration_vector=[0,0,0],label = 'Sol',size=10)
    mercurio = CreateBodyGrav(0.0553,position_vector=[0.3074866310160428,0,0],velocity_vector=[0,12.43951652406417,0],acceleration_vector=[0,0,0],label = 'Mercúrio',size = 5)
    venus = CreateBodyGrav(0.815,position_vector=[0.7184491978609626,0,0],velocity_vector=[0,7.437974438502673,0],acceleration_vector=[0,0,0],label = 'Vênus',size = 5)
    terra = CreateBodyGrav(1,position_vector=[0.9832553475935829,0,0],velocity_vector=[0,6.3895702139037430,0],acceleration_vector=[0,0,0],label = 'Terra',size=5)
    marte = CreateBodyGrav(0.107,position_vector=[1.3813502673796791,0,0],velocity_vector=[0,5.590082887700534,0],acceleration_vector=[0,0,0],label = 'Marte',size = 5)
    jupiter = CreateBodyGrav(317.83,position_vector=[4.950501336898395,0,0],velocity_vector=[0,2.894186310160428,0],acceleration_vector=[0,0,0],label = 'Júpiter',size = 5)
    saturno = CreateBodyGrav(95.16,position_vector=[9.074558823529411,0,0],velocity_vector=[0,2.138997754010695,0],acceleration_vector=[0,0,0],label = 'Saturno',size = 5)
    urano = CreateBodyGrav(14.54,position_vector=[18.26668449197861,0,0],velocity_vector=[0,1.50404871657754,0],acceleration_vector=[0,0,0],label = 'Urano',size = 5)
    netuno = CreateBodyGrav(17.15,position_vector=[29.886697860962567,0,0],velocity_vector=[0,1.153877486631016,0],acceleration_vector=[0,0,0],label = 'Netuno',size = 5)
    plutao = CreateBodyGrav(1,position_vector=[29.645635026737967,0,0],velocity_vector=[0,1.2867737967914437,0],acceleration_vector=[0,0,0],label = 'Plutão',size = 5)

    scene = GravitySim([sol,mercurio,venus,terra,marte,jupiter,saturno,urano,netuno,plutao], G = 0.00011855835621470008)

    scene.simulate([0,100], dt=1e-3, method='verlet')

    scene.showScene(dtStepPerFrame=4)
