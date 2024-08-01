import numpy as np
import matplotlib.pyplot as plt

currChDataI = np.array([])
currChDataQ = np.array([])


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
#plt.ion()

line1, = ax1.plot([], [], label='I Channel')
line2, = ax1.plot([], [], label='Q Channel')
ax1.set_xlabel('time (samples)')
ax1.set_ylabel('ADC time domain output')
ax1.set_title('Time Domain Output')
ax1.legend()
ax1.grid(True)

ax2.set_xlabel('Doppler(m/s)')
ax2.set_ylabel('Range(meters)')
ax2.set_title('Range Doppler Output')
ax2.legend()
ax2.grid(True)

def update_rangeprofile_plot(I_data, Q_data):
    line1.set_ydata(I_data)
    line2.set_ydata(Q_data)
    line1.set_xdata(np.arange(len(I_data)))
    line2.set_xdata(np.arange(len(Q_data)))
    ax1.relim()
    ax1.autoscale_view()
    plt.draw()
    plt.pause(0.01)