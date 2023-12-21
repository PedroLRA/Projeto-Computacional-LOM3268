from body import CreateBodyPen
from pendulumSim import PendulumSim

#Create bodies objects
body1 = CreateBodyPen(1,0, 1, 120, 10)
body2 = CreateBodyPen(1,0, 1, -10, 10)

#Create the scene object
scene = PendulumSim(body1, body2)

#Calculate the new positions
scene.simulate([0,10], dt = 0.01)

#Plot the scene
scene.showScene(dtStepPerFrame=1, use_lines=True)

