import numpy as np
import matplotlib.pyplot as plt
from queue import Queue


# 큐를 생성하여 전역적으로 접근할 수 있도록 설정
plot_queue = Queue()

currChDataI = np.array([])
currChDataQ = np.array([])
rangeArray = np.array([])
dopplerArray = np.array([])
rangeDoppler = np.array([])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

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

def update_rangedoppler_plot(rangeArray, dopplerArray, rangeDoppler):
    ax2.cla()
    cs = ax2.contourf(rangeArray, dopplerArray, rangeDoppler, cmap='jet')
    # fig.colorbar(cs, ax=ax2, shrink=0.9)
    ax2.grid(True)
    plt.draw()
    plt.pause(0.01)

def update_plot(currChDataI, currChDataQ, rangeArray, dopplerArray, rangeDoppler):
    # 데이터를 큐에 넣어서 메인 스레드에서 처리하도록 함
    plot_queue.put((currChDataI, currChDataQ, rangeArray, dopplerArray, rangeDoppler))

def process_plot_queue():
    while not plot_queue.empty():
        currChDataI, currChDataQ, rangeArray, dopplerArray, rangeDoppler = plot_queue.get()
        update_rangeprofile_plot(currChDataI, currChDataQ)
        update_rangedoppler_plot(rangeArray, dopplerArray, rangeDoppler)
        plt.draw()