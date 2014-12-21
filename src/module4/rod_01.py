import sys

import numpy as np
import matplotlib.pyplot as plt


def ftcs(T, nt, dt, dx, alpha):
    for n in xrange(nt):  
        Tn      = T.copy() 
        T[1:-1] = Tn[1:-1] + alpha * dt / (dx ** 2) * (Tn[2:] - 2 * Tn[1:-1] + Tn[0:-2])
        
    return T


def ftcs_mixed(T, nt, dt, dx, alpha):
    for n in xrange(nt):  
        Tn      = T.copy() 
        T[1:-1] = Tn[1:-1] + alpha * dt / (dx ** 2) * (Tn[2:] - 2 * Tn[1:-1] + Tn[0:-2])
        T[-1]   = T[-2]
        
    return T


def plot(T, x, filename):
    plt.clf()
    plt.plot(x, T, color = '#003366', ls = '-', lw = 3)
    plt.ylim(0, 100)
    plt.xlabel('Length of Rod')
    plt.ylabel('Temperature')
    plt.savefig('./src/module4/images/' + filename, format = 'png')
    plt.close()


def main(argv):
    L     = 1.0
    sigma = 0.5
    alpha = 1.22e-3

    nx    = 51
    dx    = L / (nx - 1)
    nt    = 1000
    dt    = sigma * dx * dx / alpha

    x     = np.linspace(0, L, nx)

    Ti    = np.zeros(nx)
    Ti[0] = 100

    T     = Ti.copy()
    T     = ftcs(T, nt, dt, dx, alpha)
    plot(T, x, 'rod_01.png')

    T     = Ti.copy()
    T     = ftcs_mixed(T, nt, dt, dx, alpha)
    plot(T, x, 'rod_02.png')



if __name__ == "__main__":
    main(sys.argv[1:])
