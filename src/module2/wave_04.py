import sys

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from sympy.utilities.lambdify import lambdify
from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16


def main(argv):
    x, nu, t = sp.symbols('x nu t')
    phi      = sp.exp(-((x - 4 * t) ** 2) / (4 * nu * (t + 1))) + sp.exp(-((x - 4 * t - 2 * np.pi) ** 2) / (4 * nu * (t + 1)))
    phiprime = phi.diff(x)
    func     = -2 * nu * (phiprime / phi) + 4
    ufunc    = lambdify((t, x, nu), func)

    nx       = 101
    nt       = 100
    dx       = 2 * np.pi / (nx - 1)
    nu       = 0.07
    dt       = dx * nu

    x  = np.linspace(0, 2 * np.pi, nx)
    un = np.empty(nx)
    t  = 0.0
    u  = np.asarray([ufunc(t, x0, nu) for x0 in x])

    plt.figure(figsize = (8, 5), dpi = 100)
    plt.plot(x, u, color = '#003366', ls = '--', lw = 3)
    plt.xlim([0, 2 * np.pi])
    plt.ylim([0, 10])
    plt.show()


    for n in xrange(nt):
        un = u.copy()
        u[1:-1] = un[1:-1] - un[1:-1] * (dt / dx) * (un[1:-1] - un[:-2]) + nu * (dt / dx) ** 2 *(un[2:] - 2 * un[1:-1] + un[:-2])
        u[0]    = un[0] - un[0] * (dt / dx) * (un[0] - un[-1]) + nu * (dt / dx) ** 2 * (un[1] - 2 * un[0] + un[-1])
        u[-1]   = un[-1] - un[-1] * (dt / dx) * (un[-1] - un[-2]) + nu * (dt / dx) ** 2 * (un[0]- 2 * un[-1] + un[-2])

    u_analytical = np.asarray([ufunc(nt * dt, xi, nu) for xi in x])

    plt.figure(figsize = (8, 5), dpi = 100)
    plt.plot(x, u, color = '#003366', ls = '--', lw = 3, label = 'Computational')
    plt.plot(x, u_analytical, label = 'Analytical')
    plt.xlim([0, 2 * np.pi])
    plt.ylim([0, 10])
    plt.legend()
    plt.show()



if __name__ == "__main__":
    main(sys.argv[1:])
