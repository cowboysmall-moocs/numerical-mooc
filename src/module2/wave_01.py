import sys

import numpy as np
import matplotlib.pyplot as plt                 

from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16


def main(argv):
    nx = 41  # try changing this number from 41 to 81 and Run All ... what happens?
    nt = 25
    dx = 2.0 / (nx - 1)
    dt = 0.02

    u  = np.ones(nx)      #numpy function ones()
    u[0.5 / dx : 1 / dx + 1] = 2  #setting u = 2 between 0.5 and 1 as per our I.C.s

    plt.plot(np.linspace(0, 2, nx), u, color = '#003366', ls = '--', lw = 3)
    plt.ylim(0, 2.5)
    plt.show()

    for n in xrange(nt):
        un    = u.copy()
        u[1:] = un[1:] - un[1:] * (dt / dx) * (un[1:] - un[0:-1])
        u[0]  = 1.0

    plt.plot(np.linspace(0, 2, nx), u, color = '#003366', ls = '--', lw = 3)
    plt.ylim(0, 2.5)
    plt.show()



if __name__ == "__main__":
    main(sys.argv[1:])
