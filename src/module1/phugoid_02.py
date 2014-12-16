import sys

import numpy as np
import matplotlib.pyplot as plt

from euler import numerical_solution


def fugoid_numerical(u, time, zt = 100., z0 = 100., v = 10., g = 9.81):
    return np.array([u[1], g * (1 - u[0] / zt)])


def fugoid_analytic(steps, zt = 100., z0 = 100., v = 10., g = 9.81):
    return v * ((zt / g) ** 0.5 * np.sin((g / zt) ** 0.5 * steps)) + ((z0 - zt) * np.cos((g / zt) ** 0.5 * steps)) + zt


def get_error(numeric, analytic, delta):
    return delta * np.sum(np.abs(numeric - analytic))


def plot_error(deltas, errors, filename):
    plt.clf()
    plt.figure(figsize = (10, 6), facecolor = 'w')
    plt.grid(True)
    plt.tick_params(axis = 'both', labelsize = 14)
    plt.xlabel('$\Delta t$', fontsize = 14)
    plt.ylabel('Error', fontsize = 14)
    plt.loglog(deltas, errors, 'ko-')
    plt.axis('equal')
    plt.savefig('./src/module1/images/' + filename, format = 'png')
    plt.close()


def main(argv):
    deltas = np.array([0.1, 0.05, 0.01, 0.005, 0.001, 0.0001])
    errors = np.empty_like(deltas)

    for i, delta in enumerate(deltas):
        numerical  = numerical_solution(100.0, delta, fugoid_numerical, [100., 10.])
        analytical = fugoid_analytic(numerical[:, 0])
        errors[i]  = get_error(numerical[:, 1], analytical, delta)

    plot_error(deltas, errors, 'phugoid_errors.png')


if __name__ == "__main__":
    main(sys.argv[1:])
