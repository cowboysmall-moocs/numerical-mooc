import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation



def u_initial(nx):
    u = np.ones(nx)
    u[(nx - 1) * 0.5:] = 0
    return u



def computeF(u):
    return (u ** 2) / 2



def maccormack_damped(u, nt, dt, dx, e):
    un    = np.zeros((nt, len(u)))
    un[:] = u.copy()
    ustar = u.copy()

    for n in xrange(1, nt):
        F           = computeF(u)
        ustar[1:-1] = u[1:-1] - (dt / dx) * (F[2:] - F[1:-1]) + e * (u[2:] - (2 * u[1:-1]) + u[:-2])
        Fstar       = computeF(ustar)
        un[n, 1:]   = 0.5 * (u[1:] + ustar[1:] - (dt / dx) * (Fstar[1:] - Fstar[:-1]))
        u           = un[n].copy()

    return un



def main(argv):
    nx    = 81
    nt    = 70
    dx    = 4.0 / (nx - 1)

    def animate(data):
        x = np.linspace(0, 4, nx)
        y = data

        line.set_data(x, y)
        return line,

    u     = u_initial(nx)

    sigma = 0.5
    dt    = sigma * dx


    e     = 0.5
    un    = maccormack_damped(u, nt, dt, dx, e)

    fig   = plt.figure()
    ax    = plt.axes(xlim = (0, 4), ylim = (-0.5, 2))
    line, = ax.plot([], [], lw = 2)
    anim  = animation.FuncAnimation(fig, animate, frames = un, interval = 50)
    plt.show()



if __name__ == "__main__":
    main(sys.argv[1:])
