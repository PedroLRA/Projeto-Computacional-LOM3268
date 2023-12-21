import numpy as np

class CreateBodyGrav:
    """
    Creates an object of type Body, which corresponds to a spherical body where all the necessary information for the simulation will be stored.
    
    Takes the following variables as initialization values:
        - mass: Mass of the body
            float or int
        - position_vector: Initial position of the body
            [x, y, z]
        - velocity_vector: Initial velocity of the body
            [x, y, z]
        - acceleration_vector: Initial acceleration of the body
            [x, y, z]
        - size: Size of the body
            float or int
        - label: name of the body in the legend
            str

    """

    def __init__(self, mass, position_vector, velocity_vector = [0,0,0], acceleration_vector=[0,0,0], size = 1, label = 'body',):
        self.mass = mass
        self.position = np.array(position_vector, dtype=float)
        self.velocity = np.array(velocity_vector, dtype=float)
        self.acceleration = np.array(acceleration_vector, dtype=float)
        self.label = label
        self.size = size

    def __str__(self) -> str:
        return f'\nBody type object\n\tmass = {self.mass}\n\tposition = {self.position}\n\tvelocity = {self.velocity}\n\tacceleration = {self.acceleration}\n\tsize = {self.size}\n'

class CreateBodyPen:
    """ 
    Creates an object of type Body, which corresponds to a spherical body where all the necessary information for the simulation will be stored.
    
    Takes the following variables as initialization values:
        - mass: Mass of the body
            float or int
        - w : angular velocity of the body   
            float or int
        - length: size of the rope/rod
            float or int
        - theta: initial angle of the pendulum
            float or int
        - size: Size of the body
            float or int
        - label: name of the body in the legend
            str

    """

    def __init__(self, mass,  w, length, theta, size = None, label = 'body',):
        self.mass = mass
        self.w = w
        self.length = length
        self.theta = theta
        self.label = label
        if not size:
            self.size = mass
        else:
            self.size = size

    #def __str__(self) -> str:  ALTERAR
    #    return f'\nBody type object\n\tmass = {self.mass}\n\tposition = {self.position}\n\tvelocity = {self.velocity}\n\tacceleration = {self.acceleration}\n\tsize = {self.size}\n'


if __name__ == "__main__":

    corpo1 = CreateBodyPen(1,0, 1, 120, 10)

    print(corpo1)


