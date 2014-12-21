import sys

import numpy as np
import matplotlib.pyplot as plt

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


def plot_error(nx_values, error, filename):
    plt.clf()
    plt.figure(figsize = (6, 6))
    plt.grid(True)
    plt.xlabel(r'$n_x$', fontsize = 18)
    plt.ylabel(r'$L_2$-norm of the error', fontsize = 18)
    plt.xlim(1e-4, 1)
    plt.ylim(1e-4, 1)
    plt.axis('equal')
    plt.loglog(nx_values, error, color = 'k', ls = '--', lw = 2, marker = 'o')
    plt.savefig('./src/module4/images/' + filename, format = 'png')
    plt.close()


def main(argv):
    L         = 1.0
    alpha     = 1.22e-3

    t_final   = 20.0
    dt        = 0.1
    nt        = int(t_final / dt)

    nx_values = np.asarray([11, 21, 41, 81, 161])
    error     = np.zeros(len(nx_values))

    for i, nx in enumerate(nx_values):
        dx       = L / (nx - 1)
        sigma    = alpha * dt / (dx * dx)

        x        = np.linspace(0, L, nx)

        T        = np.zeros(nx)
        T[0]     = 100

        A        = rod_03.generateMatrix(nx, sigma)
        T        = rod_03.CrankNicolson(T, A, nt, sigma)
        T_exact  = T_analytical(x, t_final, 100, alpha, L)
        error[i] = L2_error(T, T_exact)

    plot_error(nx_values, error, 'error_02.png')



if __name__ == "__main__":
    main(sys.argv[1:])
