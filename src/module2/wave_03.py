import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16


def main(argv):
    nx    = 41
    nt    = 20
    dx    = 2.0 / (nx - 1)
    nu    = 0.3   #the value of viscosity
    sigma = 0.2

    dt    = sigma * dx ** 2 / nu 
    x     = np.linspace(0, 2, nx)
    u     = np.ones(nx)      

    u[0.5 / dx : 1 / dx + 1] = 2

    for n in xrange(1, nt):
        un      = u.copy()
        u[1:-1] = un[1:-1] + nu * (dt / dx ** 2) * (un[2:] -2 * un[1:-1] + un[0:-2])

    plt.plot(np.linspace(0, 2, nx), u, color = '#003366', ls = '--', lw = 3)
    plt.ylim(0, 2.5)
    plt.show()



if __name__ == "__main__":
    main(sys.argv[1:])
