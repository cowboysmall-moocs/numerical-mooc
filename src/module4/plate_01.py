import sys

import numpy as np
import matplotlib.pyplot as plt

from scipy.linalg import solve


def ftcs(T, nt, alpha, dt, dx, dy):

    j_mid = (np.shape(T)[0]) / 2
    i_mid = (np.shape(T)[1]) / 2
    
    for n in range(nt):
        Tn            = T.copy()
        T_1           = Tn[2:, 1:-1] - 2 * Tn[1:-1, 1:-1] + Tn[:-2, 1:-1]
        T_2           = Tn[1:-1, 2:] - 2 * Tn[1:-1, 1:-1] + Tn[1:-1, :-2]
        T[1:-1, 1:-1] = Tn[1:-1, 1:-1] + alpha * (dt / (dy ** 2) * T_1 + dt / (dx ** 2) * T_2)
  
        T[-1, :]      = T[-2, :]
        T[:, -1]      = T[:, -2]
        
        if T[j_mid, i_mid] >= 70:
            print ("Center of plate reached 70C at time {0:.2f}s, in time step {1:d}.".format(dt * n, n))
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
    nt    = 500

    dx    = L / (nx - 1)
    dy    = H / (ny - 1)
    dt    = sigma * (min(dx, dy) ** 2) / alpha

    x     = np.linspace(0, L, nx)
    y     = np.linspace(0, H, ny)

    Ti       = np.ones((ny, nx)) * 20
    Ti[0, :] = 100
    Ti[:, 0] = 100

    T        = Ti.copy()
    T        = ftcs(T, nt, alpha, dt, dx, dy)

    mx, my   = np.meshgrid(x, y)
    plot(T, mx, my, 'plate_01.png')



if __name__ == "__main__":
    main(sys.argv[1:])
