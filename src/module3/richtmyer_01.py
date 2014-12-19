import sys

import numpy as np
import matplotlib.pyplot as plt


def computeU(rho, u, p, gamma):
    return np.array([[rho], [rho * u], [rho * (p / ((gamma - 1) * rho)) + ((u ** 2) / 2)]])


def computeF(u, gamma):
    f1 = u[1]
    f2 = (u[1] ** 2) / u[0]  + (gamma - 1) * (u[2] - 0.5 * (u[1] ** 2) / u[0])
    f3 = (u[2] + (gamma - 1) * (u[2] - (0.5 * u[1] ** 2) / u[0])) * (u[1] / u[0])
    return np.array([f1, f2, f3])


def plot(steps, data, title, filename):
    plt.clf()
    plt.figure(figsize = (10, 6), facecolor = 'w')
    plt.tick_params(axis = 'both', labelsize = 14)
    plt.plot(steps, data)
    plt.title(title)
    plt.savefig('./src/module3/images/' + filename, format = 'png')
    plt.close()


def main(argv):
    dx    = 0.25
    dt    = 0.0002
    nx    = 81
    nt    = int(0.01 / dt)
    gamma = 1.4

    mid   = (nx - 1) * 0.5

    x     = np.linspace(-10, 10, nx)
    u     = np.ones((3, nx))

    u[:, :mid] = computeU(1.0, 0, 100000.0, gamma)
    u[:, mid:] = computeU(0.125, 0, 10000.0, gamma)

    un    = np.ones((3, nx))
    un_h  = np.ones((3, nx))

    for i in xrange(nt):
        F_1          = computeF(u[:, 1:], gamma) - computeF(u[:, :-1], gamma)
        un_h[:, :-1] = 0.5 * (u[:, 1:] + u[:, :-1]) - ((dt / (2 * dx)) * F_1)
        F_2          = computeF(un_h[:, 1:-1], gamma) - computeF(un_h[:, :-2], gamma)
        un[:, 1:-1]  = u[:, 1:-1] - ((dt / dx) * F_2)

        un[:, 0]     = un[:, 1]
        un[:, -1]    = un[:, -2]
        u = un.copy()

    velocity = u[1, :] / u[0, :]
    pressure = (gamma - 1) * (u[2, :] - (0.5 * u[1, :] ** 2) / u[0, :])
    density  = u[0, :]

    plot(x, velocity, 'Velocity', 'velocity.png')
    plot(x, pressure, 'Pressure', 'pressure.png')
    plot(x, density, 'Density', 'density.png')

    print
    print 'Solution at 2.5m'
    print
    print 'Velocity: %0.2f' % (velocity[50])
    print 'Pressure: %0.2f' % (pressure[50])
    print ' Density: %0.2f' % (density[50])
    print


if __name__ == "__main__":
    main(sys.argv[1:])
