import numpy as np
import matplotlib.pyplot as plt

rangeArray = np.array([])
dopplerArray = np.array([])
rangeDoppler = np.array([])

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



def update_rangedoppler_plot(rangeArray,dopplerArray,rangeDoppler):
    ax2.cla()
    cs = ax2.contourf(rangeArray, dopplerArray, rangeDoppler, cmap='jet')
    #fig.colorbar(cs, ax=ax2, shrink=0.9)
    ax2.grid(True)
    plt.draw()
    plt.pause(0.01)