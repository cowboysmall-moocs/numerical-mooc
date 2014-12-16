import sys

import numpy as np

from euler import numerical_solution
from plot import plot_single


def rocket_numerical(u, time, m_s = 50.0, rho = 1.091, r = 0.5, g = 9.81, v_e = 325.0, C_d = 0.15, m_po = 100.0):
    A = np.pi * (r ** 2.0)

    if time < 5.0:
        m_p_dot = 20.0
        m_p     = m_po - (m_p_dot * time)
    else:
        m_p_dot = 0.0
        m_p     = 0.0

    h = u[1]
    v = -g + ((m_p_dot * v_e) - (0.5 * rho * u[1] * np.abs(u[1]) * A * C_d)) / (m_s + m_p)

    return np.array([h, v])


def print_results(results, index1, index2, index3):
    print 
    print ' maximum velocity: %0.2f' % (results[index1, 2])
    print '             time: %0.2f' % (results[index1, 0])
    print '         altitude: %0.2f' % (results[index1, 1])
    print 
    print '   maximum height: %0.2f' % (results[index2, 1])
    print '             time: %0.2f' % (results[index2, 0])
    print 
    print '   time of impact: %0.2f' % (results[index3, 0])
    print '         velocity: %0.2f' % (results[index3, 2])
    print


def main(argv):
    results  = numerical_solution(40.0, 0.1, rocket_numerical, [0., 0.])

    steps    = results[:, 0]
    altitude = results[:, 1]
    velocity = results[:, 2]

    index1   = np.argmax(velocity)
    index2   = np.argmax(altitude)
    index3   = np.where(altitude < 0.0)[0][0]

    print_results(results, index1, index2, index3)

    plot_single(steps, altitude, ['Altitude'], 'rocket_altitude_02.png')
    plot_single(steps, velocity, ['Velocity'], 'rocket_velocity_02.png')


if __name__ == "__main__":
    main(sys.argv[1:])
