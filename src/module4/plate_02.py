import sys

import numpy as np
import matplotlib.pyplot as plt

from scipy.linalg import solve


def constructMatrix(nx, ny, sigma):
    A = np.zeros(((nx - 2) * (ny - 2), (nx - 2) * (ny - 2)))

    row_number = 0
    for j in range(1, ny - 1):
        for i in range(1, nx - 1):
            if i == 1 and j == 1:
                A[row_number, row_number]            = 1 / sigma + 4
                A[row_number, row_number+1]          = -1
                A[row_number, row_number + (nx - 2)] = -1
            elif i == nx - 2 and j == 1:
                A[row_number, row_number]            = 1 / sigma + 3
                A[row_number, row_number - 1]        = -1
                A[row_number, row_number + (nx - 2)] = -1
            elif i == 1 and j == ny - 2:
                A[row_number, row_number]            = 1 / sigma + 3
                A[row_number, row_number + 1]        = -1
                A[row_number, row_number - (nx - 2)] = -1
            elif i == nx - 2 and j == ny - 2:
                A[row_number, row_number]            = 1 / sigma + 2
                A[row_number, row_number - 1]        = -1
                A[row_number, row_number - (nx - 2)] = -1
            elif i == 1:
                A[row_number, row_number]            = 1 / sigma + 4
                A[row_number, row_number + 1]        = -1
                A[row_number, row_number + (nx - 2)] = -1
                A[row_number, row_number - (nx - 2)] = -1
            elif i == nx - 2:
                A[row_number, row_number]            = 1 / sigma + 3
                A[row_number, row_number - 1]        = -1
                A[row_number, row_number + (nx - 2)] = -1
                A[row_number, row_number - (nx - 2)] = -1
            elif j == 1:
                A[row_number, row_number]            = 1 / sigma + 4
                A[row_number, row_number + 1]        = -1
                A[row_number, row_number - 1]        = -1
                A[row_number, row_number + (nx - 2)] = -1
            elif j == ny - 2:
                A[row_number, row_number]            = 1 / sigma + 3
                A[row_number, row_number + 1]        = -1
                A[row_number, row_number - 1]        = -1
                A[row_number, row_number - (nx - 2)] = -1
            else:
                A[row_number, row_number]            = 1 / sigma + 4
                A[row_number, row_number + 1]        = -1
                A[row_number, row_number - 1]        = -1
                A[row_number, row_number + (nx - 2)] = -1
                A[row_number, row_number - (nx - 2)] = -1
            row_number += 1
    return A 


def generateRHS(nx, ny, sigma, T, T_bc):
    RHS = np.zeros((nx - 2) * (ny - 2))

    row_number = 0
    for j in range(1, ny - 1):
        for i in range(1, nx - 1):
            if i == 1 and j == 1:
                RHS[row_number] = T[j, i] * 1 / sigma + 2 * T_bc
            elif i == nx - 2 and j == 1:
                RHS[row_number] = T[j, i] * 1 / sigma + T_bc
            elif i == 1 and j == ny - 2:
                RHS[row_number] = T[j, i] * 1 / sigma + T_bc
            elif i == nx - 2 and j == ny - 2:
                RHS[row_number] = T[j, i] * 1 / sigma
            elif i == 1:
                RHS[row_number] = T[j, i] * 1 / sigma + T_bc
            elif i == nx - 2:
                RHS[row_number] = T[j, i] * 1 / sigma
            elif j == 1:
                RHS[row_number] = T[j, i] * 1 / sigma + T_bc
            elif j == ny - 2:
                RHS[row_number] = T[j, i] * 1 / sigma
            else:
                RHS[row_number] = T[j, i] * 1 / sigma
            row_number += 1

    return RHS


def map_1Dto2D(nx, ny, T_1D, T_bc):
    T = np.zeros((ny, nx))

    row_number = 0
    for j in range(1, ny - 1):
        for i in range(1, nx - 1):
            T[j, i] = T_1D[row_number]
            row_number += 1

    T[0, :] = T_bc
    T[:, 0] = T_bc

    T[-1, :] = T[-2, :]
    T[:, -1] = T[:, -2]

    return T


def btcs_2D(T, A, nt, sigma, T_bc, nx, ny, dt):
    j_mid = (np.shape(T)[0]) / 2
    i_mid = (np.shape(T)[1]) / 2

    for t in range(nt):
        Tn         = T.copy()
        b          = generateRHS(nx, ny, sigma, Tn, T_bc)
        T_interior = solve(A, b)
        T          = map_1Dto2D(nx, ny, T_interior, T_bc)
        
        if T[j_mid, i_mid] >= 70:
            print ("Center of plate reached 70C at time {0:.2f}s, in time step {1:d}.".format(dt * t, t))
            break

    if T[j_mid, i_mid] < 70:
        print ("Center has not reached 70C yet, it is only {0:.2f}C.".format(T[j_mid, i_mid]))

    return T


def plot(T, mx, my, filename):
    plt.clf()
    plt.figure(figsize = (8, 5))
    plt.contourf(my, mx, T, 20)
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.colorbar()
    plt.savefig('./src/module4/images/' + filename, format = 'png')
    plt.close()



def main(argv):
    L     = 1.0e-2
    H     = 1.0e-2
    sigma = 0.25
    alpha = 1e-4

    nx    = 21
    ny    = 21
    nt    = 300

    dx    = L / (nx - 1)
    dy    = H / (ny - 1)
    dt    = sigma * (min(dx, dy) ** 2) / alpha

    x     = np.linspace(0, L, nx)
    y     = np.linspace(0, H, ny)

    T_bc  = 100

    Ti       = np.ones((ny, nx)) * 20
    Ti[0, :] = T_bc
    Ti[:, 0] = T_bc

    A        = constructMatrix(nx, ny, sigma)
    T        = Ti.copy()
    T        = btcs_2D(T, A, nt, sigma, T_bc, nx, ny, dt)

    mx, my   = np.meshgrid(x, y)
    plot(T, mx, my, 'plate_02.png')


if __name__ == "__main__":
    main(sys.argv[1:])
