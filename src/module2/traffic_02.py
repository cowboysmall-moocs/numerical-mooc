import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16



def velocities(v_max, rho_max, rhos):
    return [((v_max - rho_c * v_max / rho_max) * 1000.0 / 3600.0) for rho_c in rhos]



def traffic_numerical(v_max, rho_max, rho_b, dt, dx, nx, count):
    rho_0        = np.ones(nx) * rho_b
    rho_0[10:20] = 50.0

    for n in xrange(count):
        F         = v_max * rho_0 * (1.0 - (rho_0 / rho_max))
        rho_0[1:] = rho_0[1:] - (dt / dx) * (F[1:] - F[0:-1])
        rho_0[0]  = rho_b

    return rho_0



def main(argv):
    L        = 11.0
    rho_max  = 250.0
    nx       = 51
    dx       = L / (nx - 1)
    dt       = 0.001


    v_max    = 80.0

    print
    print '80 km / hr'
    results = traffic_numerical(v_max, rho_max, 10.0, dt, dx, nx, 0)
    print 'minimum velocity at t = 0 minutes: %0.2f' % np.min(velocities(v_max, rho_max, results))

    nt = int(0.05 / dt)
    results = traffic_numerical(v_max, rho_max, 10.0, dt, dx, nx, nt)
    print 'average velocity at t = 3 minutes: %0.2f' % np.mean(velocities(v_max, rho_max, results))

    nt = int(0.1 / dt)
    results = traffic_numerical(v_max, rho_max, 10.0, dt, dx, nx, nt)
    print 'minimum velocity at t = 6 minutes: %0.2f' % np.min(velocities(v_max, rho_max, results))
    print



    v_max    = 136.0

    print '136 km / hr'
    results = traffic_numerical(v_max, rho_max, 20.0, dt, dx, nx, 0)
    print 'minimum velocity at t = 0 minutes: %0.2f' % np.min(velocities(v_max, rho_max, results))

    nt = int(0.05 / dt)
    results = traffic_numerical(v_max, rho_max, 20.0, dt, dx, nx, nt)
    print 'average velocity at t = 3 minutes: %0.2f' % np.mean(velocities(v_max, rho_max, results))

    nt = int(0.05 / dt)
    results = traffic_numerical(v_max, rho_max, 20.0, dt, dx, nx, nt)
    print 'minimum velocity at t = 3 minutes: %0.2f' % np.min(velocities(v_max, rho_max, results))
    print



if __name__ == "__main__":
    main(sys.argv[1:])
