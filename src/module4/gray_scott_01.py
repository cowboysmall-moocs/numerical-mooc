import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation, cm


def gray_scott(U, V, Du, Dv, F, k):
    n  = 192
    dh = 5.0 / (n - 1)

    T  = 8000
    dt = 0.9 * (dh ** 2) / (4 * max(Du, Dv))
    nt = int(T / dt)

    D  = np.zeros((int(nt / 100) + 1, n, n))

    for n in xrange(nt):
        Un  = U.copy()
        Vn  = V.copy()

        R_1 = Un[1:-1, 1:-1] * (Vn[1:-1, 1:-1] ** 2)
        F_1 = F * (1 - Un[1:-1, 1:-1])
        F_2 = (F + k) * Vn[1:-1, 1:-1]

        U_1 = (Un[2:, 1:-1] - 2 * Un[1:-1, 1:-1] + Un[:-2, 1:-1]) / (dh ** 2)
        U_2 = (Un[1:-1, 2:] - 2 * Un[1:-1, 1:-1] + Un[1:-1, :-2]) / (dh ** 2)

        U[1:-1, 1:-1]      = Un[1:-1, 1:-1] + dt * (Du * (U_1 + U_2) - R_1 + F_1)
        U[-1, :], U[:, -1] = U[-2, :], U[:, -2]
        U[0, :], U[:, 0]   = U[1, :], U[:, 1]

        V_1 = (Vn[2:, 1:-1] - 2 * Vn[1:-1, 1:-1] + Vn[:-2, 1:-1]) / (dh ** 2)
        V_2 = (Vn[1:-1, 2:] - 2 * Vn[1:-1, 1:-1] + Vn[1:-1, :-2]) / (dh ** 2)

        V[1:-1, 1:-1]      = Vn[1:-1, 1:-1] + dt * (Dv * (V_1 + V_2) + R_1 - F_2)
        V[-1, :], V[:, -1] = V[-2, :], V[:, -2]
        V[0, :], V[:, 0]   = V[1, :], V[:, 1]

        if n % 100 == 0:
            D[n / 100] = U

    return U, V, D


def print_results(out):
    print
    print '  First: %0.4f' % out[0]
    print ' Second: %0.4f' % out[1]
    print '  Third: %0.4f' % out[2]
    print ' Fourth: %0.4f' % out[3]
    print '  Fifth: %0.4f' % out[4]
    print


def plot_results(data, filename):
    fig = plt.figure(dpi = 72)
    # fig = plt.figure(figsize = (576, 360), dpi = 72)
    # fig = plt.figure(figsize = (5, 4), dpi = 72)
    img = plt.imshow(data[0], cmap = cm.RdBu)

    def animate(data):
        img.set_array(data)
        return img,

    anim = animation.FuncAnimation(fig, animate, frames = data, interval = 85)
    # anim = animation.FuncAnimation(fig, animate, frames = data, interval = 85, blit = True)
    # anim.save('./src/module4/images/' + filename, writer = 'imagemagick', fps = 30)
    plt.show()


def main(argv):
    data    = np.load('./src/module4/data/uvinitial.npz')
    U       = data['U']
    V       = data['V']

    U, V, D = gray_scott(U, V, 0.00016, 0.00008, 0.035, 0.065) # Bacteria 1
    # U, V, D = gray_scott(U, V, 0.00014, 0.00006, 0.035, 0.065) # Bacteria 2
    # U, V, D = gray_scott(U, V, 0.00016, 0.00008, 0.060, 0.062) # Coral
    # U, V, D = gray_scott(U, V, 0.00019, 0.00005, 0.060, 0.062) # Fingerprint
    # U, V, D = gray_scott(U, V, 0.00010, 0.00010, 0.018, 0.050) # Spirals
    # U, V, D = gray_scott(U, V, 0.00012, 0.00008, 0.020, 0.050) # Spirals Dense
    # U, V, D = gray_scott(U, V, 0.00010, 0.00016, 0.020, 0.050) # Spirals Fast
    # U, V, D = gray_scott(U, V, 0.00016, 0.00008, 0.020, 0.055) # Unstable
    # U, V, D = gray_scott(U, V, 0.00016, 0.00008, 0.050, 0.065) # Worms 1
    # U, V, D = gray_scott(U, V, 0.00016, 0.00008, 0.054, 0.063) # Worms 2
    # U, V, D = gray_scott(U, V, 0.00016, 0.00008, 0.035, 0.060) # Zebrafish

    print_results(U[100, ::40])
    plot_results(D, 'gray_scott_01.gif')


if __name__ == "__main__":
    main(sys.argv[1:])
