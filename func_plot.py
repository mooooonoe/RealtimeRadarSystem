import numpy as np
import matplotlib.pyplot as plt
from queue import Queue

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
