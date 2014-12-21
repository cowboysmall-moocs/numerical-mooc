import sys

import numpy as np
import matplotlib.pyplot as plt

from scipy.linalg import solve


def generateMatrix(N, sigma):
    d         = 2 * np.diag(np.ones(N - 2) * (1 + 1.0 / sigma))
    d[-1, -1] = 1 + 2.0 / sigma
    ud        = np.diag(np.ones(N - 3) * -1, 1)
    ld        = np.diag(np.ones(N - 3) * -1, -1)
    return d + ud + ld


def generateRHS(T, sigma):
    b     = T[1:-1] * 2 * (1.0 / sigma - 1) + T[:-2] + T[2:]
    b[0] += T[0]
    return b


def CrankNicolson(T, A, nt, sigma):
    for t in xrange(nt):
        Tn         = T.copy()
        b          = generateRHS(Tn, sigma)
        T_interior = solve(A, b)
        T[1:-1]    = T_interior
        T[-1]      = T[-2]

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

    nx    = 21
    dx    = L / (nx - 1)
    nt    = 10
    dt    = sigma * dx * dx / alpha

    x     = np.linspace(0, L, nx)

    Ti    = np.zeros(nx)
    Ti[0] = 100

    A     = generateMatrix(nx, sigma)

    T     = Ti.copy()
    T     = CrankNicolson(T, A, nt, sigma)
    plot(T, x, 'rod_04.png')



if __name__ == "__main__":
    main(sys.argv[1:])
