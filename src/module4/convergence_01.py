import sys

import numpy as np
import matplotlib.pyplot as plt

import rod_02
import rod_03

from scipy.linalg import solve
from math import pi


def T_analytical(x, t, n_max, alpha, L):
    T = 100
    for n in xrange(1, n_max + 1):
        k         = (2 * n - 1) * pi / (2 * L)
        summation = 400 / ((2 * n - 1) * pi) * np.sin(k * x) * np.exp(-alpha * k * k * t)
        T        -= summation

    return T


def L2_error(T, T_exact):
    return np.sqrt(np.sum((T - T_exact) ** 2) / np.sum(T_exact) ** 2)


def plot_error(dt_values, error1, error2, filename):
    plt.clf()
    plt.figure(figsize = (6, 6))
    plt.grid(True)
    plt.xlabel(r'$\Delta t$', fontsize = 18)
    plt.ylabel(r'$L_2$-norm of the error', fontsize = 18)
    plt.xlim(1e-2, 1)
    plt.ylim(1e-4, 1)
    plt.axis('equal')
    plt.loglog(dt_values, error1, color = 'k', ls = '--', lw = 2, marker = 'o')
    plt.loglog(dt_values, error2, color = 'k', ls = '--', lw = 2, marker = 's')
    plt.savefig('./src/module4/images/' + filename, format = 'png')
    plt.close()


def main(argv):
    L          = 1.0
    alpha      = 1.22e-3

    nx         = 1001
    dx         = L / (nx - 1)

    x          = np.linspace(0, L, nx)

    dt_values  = np.asarray([1.0, 0.5, 0.25, 0.125])
    error      = np.zeros(len(dt_values))
    error_ftcs = np.zeros(len(dt_values))

    t_final    = 10.0 
    t_initial  = 1.0

    Ti         = T_analytical(x, t_initial, 100, alpha, L)
    T_exact    = T_analytical(x, t_final, 100, alpha, L)

    for i, dt in enumerate(dt_values):
        sigma         = alpha * dt / (dx * dx)
        nt            = int((t_final - t_initial) / dt)

        T             = Ti.copy()
        A             = rod_03.generateMatrix(nx, sigma)
        T             = rod_03.CrankNicolson(T, A, nt, sigma)
        error[i]      = L2_error(T, T_exact)

        T             = Ti.copy()
        A_ftcs        = rod_02.generateMatrix(nx, sigma)
        T             = rod_02.implicit_ftcs(T, A_ftcs, nt, sigma)
        error_ftcs[i] = L2_error(T, T_exact)

    plot_error(dt_values, error, error_ftcs, 'error_01.png')



if __name__ == "__main__":
    main(sys.argv[1:])
