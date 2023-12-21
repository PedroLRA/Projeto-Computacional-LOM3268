from body import CreateBodyGrav
from gravitySim import GravitySim

#Create bodies objects
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

#Create the scene object
scene = GravitySim([sol,mercurio,venus,terra,marte,jupiter,saturno,urano,netuno,plutao], G = 0.00011855835621470008)

#Calculate the new positions
scene.simulate([0,50], dt=1e-3, method='verlet')

#Plot the scene
scene.showScene(dtStepPerFrame=4)
