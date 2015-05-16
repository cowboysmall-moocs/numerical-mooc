import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation


def rho_green_light(nx, rho_max, rho_light):
    rho = np.arange(nx) * 2.0 / nx * rho_light
    rho[(nx - 1) / 2:] = 0
    return rho



def computeF(u_max, rho_max, rho):
    return u_max * rho * (1 - rho / rho_max)



def ftbs(rho, nt, dt, dx, rho_max, u_max):
    rho_n       = np.zeros((nt, len(rho)))      
    rho_n[0, :] = rho.copy()              
    
    for t in xrange(1, nt):
        F            = computeF(u_max, rho_max, rho)
        rho_n[t, 1:] = rho[1:] - (dt / dx) * (F[1:] - F[:-1])
        rho_n[t, 0]  = rho[0]
        rho_n[t, -1] = rho[-1]
        rho          = rho_n[t].copy()

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
    sigma = 1.0
    nx    = 81
    nt    = 40
    dx    = 4.0 / (nx - 1)
    dt    = sigma * dx

    x     = np.linspace(0, 4, nx)

    rho_max   = 10.0
    u_max     = 1.1
    rho_light = 4.0

    rho       = rho_green_light(nx, rho_max, rho_light)
    plot(x, rho, 'traffic_01.png')
    rho_n     = ftbs(rho, nt, dt, dx, rho_max, u_max)

    def animate(data):
        x = np.linspace(0, 4, nx)
        y = data
        line.set_data(x, y)
        return line,

    fig   = plt.figure(facecolor = 'w')
    ax    = plt.axes(xlim = (0, 4), ylim = (-0.5, 11.5), xlabel = ('Distance'), ylabel = ('Traffic density'))
    line, = ax.plot([],[], color = '#003366', lw = 2)
    anim  = animation.FuncAnimation(fig, animate, frames = rho_n, interval = 50)
    plt.show()



if __name__ == "__main__":
    main(sys.argv[1:])
