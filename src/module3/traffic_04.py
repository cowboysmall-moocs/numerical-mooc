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


def godunov(rho, nt, dt, dx, rho_max, V_max):
    rho_n       = np.zeros((nt, len(rho)))
    rho_n[:, :] = rho.copy()

    rho_plus    = np.zeros_like(rho)
    rho_minus   = np.zeros_like(rho)
    flux        = np.zeros_like(rho)

    for t in xrange(1, nt):
        rho_plus[:-1]  = rho[1:]
        rho_minus      = rho.copy()
        flux           = 0.5 * (computeF(V_max, rho_max, rho_minus) + computeF(V_max, rho_max, rho_plus) + (dx / dt) * (rho_minus - rho_plus))
        rho_n[t, 1:-1] = rho[1:-1] + (dt / dx) * (flux[:-2] - flux[1:-1])
        rho_n[t, 0]    = rho[0]
        rho_n[t, -1]   = rho[-1]
        rho            = rho_n[t].copy()

    return rho_n


def muscl(rho, nt, dt, dx, rho_max, V_max):
    rho_n       = np.zeros((nt, len(rho)))
    rho_n[:, :] = rho.copy()

    rho_plus    = np.zeros_like(rho)
    rho_minus   = np.zeros_like(rho)
    flux        = np.zeros_like(rho)
    rho_star    = np.zeros_like(rho)

    for t in xrange(1, nt):
        sigma          = minmod(rho, dx)
        rho_left       = rho + sigma * dx / 2.0
        rho_right      = rho - sigma * dx / 2.0
        
        flux_left      = computeF(V_max, rho_max, rho_left) 
        flux_right     = computeF(V_max, rho_max, rho_right)
        flux[:-1]      = 0.5 * (flux_right[1:] + flux_left[:-1] - (dx / dt) * (rho_right[1:] - rho_left[:-1]))
        rho_star[1:-1] = rho[1:-1] + (dt / dx) * (flux[:-2] - flux[1:-1])


        rho_star[0]    = rho[0]
        rho_star[-1]   = rho[-1]

        sigma          = minmod(rho_star, dx)
        rho_left       = rho_star + sigma * dx / 2.0
        rho_right      = rho_star - sigma * dx / 2.0

        flux_left      = computeF(V_max, rho_max, rho_left)
        flux_right     = computeF(V_max, rho_max, rho_right)
        flux[:-1]      = 0.5 * (flux_right[1:] + flux_left[:-1] - (dx / dt) * (rho_right[1:] - rho_left[:-1]))
        rho_n[t, 1:-1] = 0.5 * (rho[1:-1] + rho_star[1:-1] + (dt / dx) * (flux[:-2] - flux[1:-1]))

        rho_n[t, 0]    = rho[0]
        rho_n[t, -1]   = rho[-1]
        rho            = rho_n[t].copy()

    return rho_n


def minmod(e, dx):
    sigma    = np.zeros_like(e)
    de_minus = np.ones_like(e)
    de_plus  = np.ones_like(e)

    de_minus[1:] = (e[1:] - e[:-1]) / dx
    de_plus[:-1] = (e[1:] - e[:-1]) / dx
    
    for i in xrange(1, len(e) - 1):
        if de_minus[i] * de_plus[i] < 0.0:
            sigma[i] = 0.0
        elif np.abs(de_minus[i]) < np.abs(de_plus[i]):
            sigma[i] = de_minus[i]
        else:
            sigma[i] = de_plus[i]

    return sigma


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
    nx      = 101
    nt      = 30
    dx      = 4.0 / (nx - 2)
    x       = np.linspace(0, 4, nx - 1)

    rho_in  = 5.0
    rho_max = 10.0
    V_max   = 1.0

    dt      = sigma * dx / V_max

    rho     = rho_red_light(nx - 1, rho_max, rho_in)
    plot(x, rho, 'traffic_04.png')

    def animate(data):
        x = np.linspace(0, 4, nx - 1)
        y = data
        line.set_data(x, y)
        return line


    rho_n = godunov(rho, nt, dt, dx, rho_max, V_max)

    fig   = plt.figure(facecolor = 'w')
    ax    = plt.axes(xlim = (0, 4), ylim = (4.5, 11), xlabel = ('Distance'), ylabel = ('Traffic density'))
    line, = ax.plot([],[], color = '#003366', lw = 2)
    anim  = animation.FuncAnimation(fig, animate, frames = rho_n, interval = 50)
    plt.show()


    rho_n = muscl(rho, nt, dt, dx, rho_max, V_max)

    fig   = plt.figure(facecolor = 'w')
    ax    = plt.axes(xlim = (0, 4), ylim = (4.5, 11), xlabel = ('Distance'), ylabel = ('Traffic density'))
    line, = ax.plot([],[], color = '#003366', lw = 2)
    anim  = animation.FuncAnimation(fig, animate, frames = rho_n, interval = 50)
    plt.show()



if __name__ == "__main__":
    main(sys.argv[1:])
