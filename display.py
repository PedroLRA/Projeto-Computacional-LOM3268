import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

def show(classObject, dtStepPerFrame, use_lines=False, **kwargs):
    # Criando a cena com subplots
    fig = plt.figure(figsize=(12, 6))

    # Subplot 3D principal
    ax_3d = fig.add_subplot(121, projection='3d')
    ax_3d.set_xlabel('X')
    ax_3d.set_ylabel('Y')
    ax_3d.set_zlabel('Z')

    frameStep = dtStepPerFrame

    # Configurando os limites para os eixos no subplot 3D principal
    MaxAxisValue = np.max(np.abs(classObject.positions))
    ax_3d.set_xlim(-MaxAxisValue, MaxAxisValue)
    ax_3d.set_ylim(-MaxAxisValue, MaxAxisValue)
    ax_3d.set_zlim(-MaxAxisValue, MaxAxisValue)

    # Subplots para XY, XZ e YZ
    ax_xy = fig.add_subplot(322, aspect='equal')
    ax_xy.set_xlabel('X', rotation=0)
    ax_xy.set_ylabel('Y', rotation=0)
    ax_xy.set_xlim(-MaxAxisValue, MaxAxisValue)
    ax_xy.set_ylim(-MaxAxisValue, MaxAxisValue)

    ax_xz = fig.add_subplot(324, aspect='equal')
    ax_xz.set_xlabel('X', rotation=0)
    ax_xz.set_ylabel('Z', rotation=0)
    ax_xz.set_xlim(-MaxAxisValue, MaxAxisValue)
    ax_xz.set_ylim(-MaxAxisValue, MaxAxisValue)

    ax_yz = fig.add_subplot(326, aspect='equal')
    ax_yz.set_xlabel('Y', rotation=0)
    ax_yz.set_ylabel('Z', rotation=0)
    ax_yz.set_xlim(-MaxAxisValue, MaxAxisValue)
    ax_yz.set_ylim(-MaxAxisValue, MaxAxisValue)

    # Plotando os corpos em sua posição inicial
    plot3D = np.full(classObject.numOfBodies, None, dtype=object)
    plot2D_xy = np.full(classObject.numOfBodies, None, dtype=object)
    plot2D_xz = np.full(classObject.numOfBodies, None, dtype=object)
    plot2D_yz = np.full(classObject.numOfBodies, None, dtype=object)
    for i in range(classObject.numOfBodies):
        x, y, z = classObject.positions[i, :, 0]
        plot3D[i], = ax_3d.plot([x], [y], [z], 'o', label=classObject.bodies[i].label, markersize=classObject.bodies[i].size)
        plot2D_xy[i], = ax_xy.plot([x], [y], 'o', markersize=classObject.bodies[i].size)
        plot2D_xz[i], = ax_xz.plot([x], [z], 'o', markersize=classObject.bodies[i].size)
        plot2D_yz[i], = ax_yz.plot([y], [z], 'o', markersize=classObject.bodies[i].size)

    # Adicionando um slider para controlar o tempo na simulação
    axcolor = 'lightgoldenrodyellow'
    axSlider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(axSlider, 'Time', classObject.time[0], classObject.time[-1], valinit=classObject.time[0], valstep=classObject.dt)

    # Adicionando linhas no subplot 3D se necessário
    if use_lines:
        line, = ax_3d.plot([], [], [], color='black', linestyle='-', linewidth=2)
        line_zero_to_body, = ax_3d.plot([], [], [], color='black', linewidth=2)
        center_body, = ax_3d.plot([0], [0], [0], 'o', color='black', label='Origin Body', markersize=10)

    # Conectando a função updateDisplay quando o slider é alterado
    def updateDisplay(val):
        for i in range(classObject.numOfBodies):
            timeIndex, = np.where(abs(classObject.time - float(slider.val)) < 1e-10)[0]
            x, y, z = classObject.positions[i, :, timeIndex]
            plot3D[i].set_data([x], [y])
            plot3D[i].set_3d_properties([z])

            plot2D_xy[i].set_data([x], [y])
            plot2D_xz[i].set_data([x], [z])
            plot2D_yz[i].set_data([y], [z])

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

    # Conectar eventos de zoom do subplot 3D aos subplots 2D
    def on_3d_motion(event):
        ax_xy.set_xlim(ax_3d.get_xlim())
        ax_xy.set_ylim(ax_3d.get_ylim())
        ax_xz.set_xlim(ax_3d.get_xlim())
        ax_xz.set_ylim(ax_3d.get_zlim())
        ax_yz.set_xlim(ax_3d.get_ylim())
        ax_yz.set_ylim(ax_3d.get_zlim())

    fig.canvas.mpl_connect('motion_notify_event', on_3d_motion)

    # Criando a animação para atualizar o slider no tempo
    def updateSlider(num, slider):
        val = slider.val
        val += frameStep * classObject.dt
        if val > slider.valmax:
            val = slider.valmin
        slider.set_val(val)

    ani = FuncAnimation(fig, updateSlider, fargs=(slider,), interval=1000/60, frames=classObject.numIterations, cache_frame_data=False)

    # Adicionando botão de play/pause
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

    # Adicionando legenda ao subplot 3D principal
    fig.legend(loc='center right', borderaxespad=10)


    # plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    pass
