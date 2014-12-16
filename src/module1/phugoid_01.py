import sys

import numpy as np
import matplotlib.pyplot as plt

from euler import numerical_solution


def fugoid_numerical(u, time, zt = 100., z0 = 100., v = 10., g = 9.81):
    return np.array([u[1], g * (1 - u[0] / zt)])


def fugoid_analytic(steps, zt = 100., z0 = 100., v = 10., g = 9.81):
    return v * ((zt / g) ** 0.5 * np.sin((g / zt) ** 0.5 * steps)) + ((z0 - zt) * np.cos((g / zt) ** 0.5 * steps)) + zt


def plot_multiple(steps, datas, legends, filename):
    plt.clf()
    plt.figure(figsize = (10, 6), facecolor = 'w')
    plt.ylim(0, 1.2 * np.max(datas[0]))
    plt.tick_params(axis = 'both', labelsize = 14)
    plt.xlabel('step', fontsize = 14)
    plt.ylabel('data', fontsize = 14)
    for data in datas:
        plt.plot(steps, data)
    plt.legend(legends)
    plt.savefig('./src/module1/images/' + filename, format = 'png')
    plt.close()


def main(argv):
    numerical_result  = numerical_solution(100.0, 0.01, fugoid_numerical, [100., 10.])
    analytical_result = fugoid_analytic(numerical_result[:, 0])

    plot_multiple(numerical_result[:, 0], [numerical_result[:, 1], analytical_result], ['Numerical', 'Analytical'], 'phugoid_trajectory.png')


if __name__ == "__main__":
    main(sys.argv[1:])
