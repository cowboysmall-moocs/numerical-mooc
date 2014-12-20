import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation


def rho_red_light(nx, rho_max, rho_in):
    rho = rho_max * np.ones(nx)
    rho[:(nx - 1) * 3.0 / 4.0] = rho_in
    return rho


def computeF(u_max, rho_max, rho):
    return u_max * rho * (1 - rho / rho_max)


def laxfriedrichs(rho, nt, dt, dx, rho_max, u_max):
    rho_n       = np.zeros((nt, len(rho)))
    rho_n[:, :] = rho.copy()

    for t in xrange(1, nt):
        F              = computeF(u_max, rho_max, rho)
        rho_n[t, 1:-1] = 0.5 * (rho[2:] + rho[:-2]) - dt/(2 * dx) * (F[2:] - F[:-2])
        rho_n[t, 0]    = rho[0]
        rho_n[t, -1]   = rho[-1]

        rho = rho_n[t].copy()

    return rho_n


def Jacobian(u_max, rho_max, rho):
    return u_max * (1 - 2 * rho / rho_max)


def laxwendroff(rho, nt, dt, dx, rho_max, u_max):
    rho_n       = np.zeros((nt, len(rho)))
    rho_n[:, :] = rho.copy()
    

    for t in xrange(1, nt):
        F              = computeF(u_max, rho_max, rho)
        J              = Jacobian(u_max, rho_max, rho)
        
        D_2            = (J[2:] + J[1:-1]) * (F[2:] - F[1:-1]) - (J[1:-1] + J[:-2]) * (F[1:-1] - F[:-2])
        rho_n[t, 1:-1] = rho[1:-1] - dt / (2 * dx) * (F[2:] - F[:-2]) + ((dt / (2 * dx)) ** 2) * D_2
        
        rho_n[t, 0]    = rho[0]
        rho_n[t, -1]   = rho[-1]
        rho            = rho_n[t].copy()
        
    return rho_n


def maccormack(rho, nt, dt, dx, u_max, rho_max):
    rho_n       = np.zeros((nt, len(rho)))
    rho_star    = np.empty_like(rho)
    rho_n[:, :] = rho.copy()
    rho_star    = rho.copy()

    for t in xrange(1, nt):
        F             = computeF(u_max, rho_max, rho)
        rho_star[:-1] = rho[:-1] - (dt / dx) * (F[1:] - F[:-1])
        Fstar         = computeF(u_max, rho_max, rho_star)
        rho_n[t,1:]   = 0.5 * (rho[1:] + rho_star[1:] - (dt / dx) * (Fstar[1:] - Fstar[:-1]))
        rho           = rho_n[t].copy()

    return rho_n



def plot(x, rho, filename):
    plt.clf()
    plt.plot(x, rho, color = '#003366', ls = '-', lw = 3)
    plt.ylabel('Traffic density')
    plt.xlabel('Distance')
    plt.ylim(-0.5, 11.0)
    plt.savefig('./src/module3/images/' + filename, format = 'png')
    plt.close()


def main(argv):
    sigma   = 1.0
    nx      = 81
    nt      = 30
    dx      = 4.0 / (nx - 1)

    x       = np.linspace(0, 4, nx)

    rho_max = 10.0
    u_max   = 1.0
    rho_in  = 5.0

    dt      = sigma * dx / u_max

    rho     = rho_red_light(nx, rho_max, rho_in)
    plot(x, rho, 'traffic_02.png')

    def animate(data):
        x = np.linspace(0, 4, nx)
        y = data
        line.set_data(x, y)
        return line,


    rho_n = laxfriedrichs(rho, nt, dt, dx, rho_max, u_max)

    fig   = plt.figure()
    ax    = plt.axes(xlim = (0, 4), ylim = (4.5, 11), xlabel = ('Distance'), ylabel = ('Traffic density'))
    line, = ax.plot([], [], color = '#003366', lw = 2)
    anim  = animation.FuncAnimation(fig, animate, frames = rho_n, interval = 50)
    plt.show()


    rho_n = laxwendroff(rho, nt, dt, dx, rho_max, u_max)

    fig   = plt.figure()
    ax    = plt.axes(xlim = (0, 4), ylim = (4.5, 11), xlabel = ('Distance'), ylabel = ('Traffic density'))
    line, = ax.plot([], [], color = '#003366', lw = 2)
    anim  = animation.FuncAnimation(fig, animate, frames = rho_n, interval = 50)
    plt.show()


    rho_n = maccormack(rho, nt, dt, dx, u_max, rho_max)

    fig   = plt.figure()
    ax    = plt.axes(xlim = (0, 4), ylim = (4.5, 11), xlabel = ('Distance'), ylabel = ('Traffic density'))
    line, = ax.plot([], [], color = '#003366', lw = 2)
    anim  = animation.FuncAnimation(fig, animate, frames = rho_n, interval = 50)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
