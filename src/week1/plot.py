import numpy as np
import matplotlib.pyplot as plt


def plot_error(deltas, errors):
    plt.figure(figsize = (10, 6), facecolor = 'w')
    plt.grid(True)
    plt.tick_params(axis = 'both', labelsize = 14)
    plt.xlabel('$\Delta t$', fontsize = 14)
    plt.ylabel('Error', fontsize = 14)
    plt.loglog(deltas, errors, 'ko-')
    plt.axis('equal')
    plt.show()



def plot_multiple(steps, datas, legends):
    plt.figure(figsize = (10, 6), facecolor = 'w')
    plt.ylim(0, 1.2 * np.max(datas[0]))
    plt.tick_params(axis = 'both', labelsize = 14)
    plt.xlabel('step', fontsize = 14)
    plt.ylabel('data', fontsize = 14)
    for data in datas:
        plt.plot(steps, data)
    plt.legend(legends)
    plt.show()



def plot_single(steps, data, legend):
    plt.figure(figsize = (10, 6), facecolor = 'w')
    plt.ylim(0, 1.2 * np.max(data))
    plt.tick_params(axis = 'both', labelsize = 14)
    plt.xlabel('t', fontsize = 14)
    plt.ylabel('z', fontsize = 14)
    plt.plot(steps, data)
    plt.legend(legend)
    plt.show()
