################## Plotting #######################
#Should we made the plot in a different class/function?
# To make this we will need to define a default output for each simmulation and then create a plot method that accepts this pattern
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

def show(classObject, dtStepPerFrame, use_lines = False, **kwargs):
    #creating the scene
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    frameStep = dtStepPerFrame

    # setting limits for the axes
    MaxAxisValue = np.max(np.abs(classObject.positions))
    ax.set_xlim(-MaxAxisValue, MaxAxisValue) 
    ax.set_ylim(-MaxAxisValue, MaxAxisValue)  
    ax.set_zlim(-MaxAxisValue, MaxAxisValue)

    #plotting the bodies in their stating position
    bodiesPlot = np.full(classObject.numOfBodies, None, dtype=object)
    for i in range(classObject.numOfBodies):
        x, y, z = classObject.positions[i,:,0]
        bodiesPlot[i], = ax.plot([x], [y], [z], 'o', label=classObject.bodies[i].label, markersize = classObject.bodies[i].size)

    #adding a slider to control the time in the simmulation
    axcolor = 'lightgoldenrodyellow'
    axSlider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(axSlider, 'Time', classObject.time[0], classObject.time[-1], valinit=classObject.time[0], valstep=classObject.dt)

    if use_lines:
        line, = ax.plot([], [], [], color='black', linestyle='-', linewidth=2)
        line_zero_to_body, = ax.plot([], [], [], color='black', linewidth=2)
        center_body, = ax.plot([0], [0], [0], 'o', color='black',label='Origin Body', markersize=10)

    #conect the function updateDisplay to when the slider is changed
    def updateDisplay(val):
        for i in range(classObject.numOfBodies):
            timeIndex, = np.where(abs(classObject.time - float(slider.val)) < 1e-10)[0]
            x, y, z = classObject.positions[i,:,timeIndex]
            bodiesPlot[i].set_data([x], [y])
            bodiesPlot[i].set_3d_properties([z])

         # Update the line connecting the bodies
        if use_lines:
            x_line = classObject.positions[:, 0, timeIndex]
            y_line = classObject.positions[:, 1, timeIndex]
            z_line = classObject.positions[:, 2, timeIndex]
            line.set_data(x_line, y_line)
            line.set_3d_properties(z_line)
            x_zero_to_body = [0, classObject.positions[0, 0, timeIndex]]
            y_zero_to_body = [0, classObject.positions[0, 1, timeIndex]]
            z_zero_to_body = [0, classObject.positions[0, 2, timeIndex]]
            line_zero_to_body.set_data(x_zero_to_body, y_zero_to_body)
            line_zero_to_body.set_3d_properties(z_zero_to_body)
           
        fig.canvas.draw_idle()
    slider.on_changed(updateDisplay)

    #creating the animation to update the slider by time
    def updateSlider(num, slider):
        val = slider.val
        val += frameStep*classObject.dt 
        if val > slider.valmax:
            val = slider.valmin
        slider.set_val(val)

    ani = FuncAnimation(fig, updateSlider, fargs=(slider,), interval=1000/60, frames=classObject.numIterations, cache_frame_data=False)

 # Adding play/pause button
    axPlayPause = plt.axes([0.1, 0.1, 0.1, 0.04])
    playPauseButton = Button(axPlayPause, 'Pause')

    def togglePlayPause(event):
        nonlocal frameStep
        if frameStep:
            playPauseButton.label.set_text('Play')
            frameStep = 0
        else:
            playPauseButton.label.set_text('Pause')
            frameStep = dtStepPerFrame

    playPauseButton.on_clicked(togglePlayPause)

    ax.legend()
    plt.show()

if __name__ == "__main__":
    pass
