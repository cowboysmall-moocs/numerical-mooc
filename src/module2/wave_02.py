import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16



def linearconv(nx):
    dx    = 2.0 / (nx - 1)
    nt    = 20
    c     = 1
    sigma = 0.5

    dt    = sigma * dx

    u     = np.ones(nx)
    u[0.5 / dx : 1 / dx + 1] = 2

    un = np.ones(nx)

    for n in xrange(nt):
        un    = u.copy()
        u[1:] = un[1:] - c * (dt / dx) * (un[1:] - un[0:-1])
        u[0]  = 1.0

    plt.plot(np.linspace(0, 2, nx), u, color = '#003366', ls = '--', lw = 3)
    plt.ylim(0, 2.5)
    plt.show()


def main(argv):
    linearconv(41) #convection using 41 grid points
    linearconv(61)
    linearconv(71)
    linearconv(81)
    linearconv(101)
    linearconv(121)


if __name__ == "__main__":
    main(sys.argv[1:])
