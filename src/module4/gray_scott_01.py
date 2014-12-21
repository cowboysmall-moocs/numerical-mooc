import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation, cm

#Du, Dv, F, k = 0.00014, 0.00006, 0.035, 0.065 # Bacteria 2
#Du, Dv, F, k = 0.00016, 0.00008, 0.060, 0.062 # Coral
#Du, Dv, F, k = 0.00019, 0.00005, 0.060, 0.062 # Fingerprint
#Du, Dv, F, k = 0.00010, 0.00010, 0.018, 0.050 # Spirals
#Du, Dv, F, k = 0.00012, 0.00008, 0.020, 0.050 # Spirals Dense
#Du, Dv, F, k = 0.00010, 0.00016, 0.020, 0.050 # Spirals Fast
#Du, Dv, F, k = 0.00016, 0.00008, 0.020, 0.055 # Unstable
#Du, Dv, F, k = 0.00016, 0.00008, 0.050, 0.065 # Worms 1
#Du, Dv, F, k = 0.00016, 0.00008, 0.054, 0.063 # Worms 2
#Du, Dv, F, k = 0.00016, 0.00008, 0.035, 0.060 # Zebrafish


def main(argv):
    Du = 0.00016
    Dv = 0.00008
    F  = 0.035 
    k  = 0.065

    n  = 192
    dh = 5.0 / (n - 1)

    T  = 8000
    dt = 0.9 * (dh ** 2) / (4 * max(Du, Dv))
    nt = int(T / dt)

    uv = np.load('./src/module4/data/uvinitial.npz')
    U  = uv['U']
    V  = uv['V']

    D  = np.zeros((int(nt / 100) + 1, len(U), len(U)))

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



    out = U[100, ::40]

    print
    print '  First: %0.4f' % out[0]
    print ' Second: %0.4f' % out[1]
    print '  Third: %0.4f' % out[2]
    print ' Fourth: %0.4f' % out[3]
    print '  Fifth: %0.4f' % out[4]
    print

    fig = plt.figure(figsize = (8, 5), dpi = 72)
    img = plt.imshow(D[0], cmap = cm.RdBu)

    def animate(data):
        img.set_array(data)
        return img,

    anim = animation.FuncAnimation(fig, animate, frames = D, interval = 85)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
