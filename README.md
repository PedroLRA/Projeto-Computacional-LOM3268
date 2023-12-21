# Double pendulum and gravitation simulation - How to use:

## 1. Download the files from this repository and put them into the desired folder.

## 2. Install the necessary libraries with the following command:

```sh
pip install numpy matplotlib pandas tqdm astropy
```

## 3. Import these modules:

```python
from body import CreateBodyGrav, CreateBodyPen
from gravitySim import GravitySim
from pendulumSim import PendulumSim

```
## 4. Gravitational systems:

### 4.1 Define the bodies of the system as it follows:

```python
Sol = CreateBodyGrav(333000,position_vector=[0,0,0],velocity_vector=[0,0,0],acceleration_vector=[0,0,0])
Terra = CreateBodyGrav(1,position_vector=[1,0,0],velocity_vector=[0,2*np.pi,0],acceleration_vector=[0,0,0])
CorpoDesconhecido = CreateBodyGrav(1,position_vector=[-2,0,0],velocity_vector=[0,-np.pi,0],acceleration_vector=[0,0,0])
```
At this stage, it is possible to use the non required parameter 'radius' to increase the visible size of the bodies

### 4.2 Create the object of the simulation with the following command:

```python
scene = GravitySim([Sol,Terra, CorpoDesconhecido], G = 0.00011855835621470008)
```

obs: G is not a required parameter, in case it is not given, the SI will be used.

### 4.3 Perform the calculations for a specific interval:

```python
scene.simulate([0, 15], dt=1e-3, method='verlet')
```

### 4.4 Finally, generate the plot of the animation, or export the information of the dataframe:

```python
#Plot
scene.showScene(dtStepPerFrame=4)
```
## 5. Double pendulum systems:

### 5.1 Define the bodies of the system as it follows:

```python
body_1 = CreateBodyPen(1,0, 1, 120, label = 'body1') #mass,  w, length, theta
body_2 = CreateBodyPen(1,0, 1, -10, label = 'body2')
```


### 5.2 Create the object of the simulation with the following command:

```python
scene = PendulumSim(corpo1, corpo2)
```


### 5.3 Perform the calculations for a specific interval:

```python
scene.simulate([0,10], dt = 0.01)
```

### 5.4 Finally, generate the plot of the animation:

```python
#Plot
scene.showScene(dtStepPerFrame=4)
```

