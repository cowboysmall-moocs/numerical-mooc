import sys

import numpy as np

from plot import plot_single, plot_multiple, plot_error


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
    m_s   = 50.0
    rho   = 1.091
    A     = np.pi * (0.5 ** 2.0)
    g     = 9.81
    v_e   = 325.0
    C_d   = 0.15
    m_po  = 100.0

    T     = 40.0
    delta = 0.1
    count = int(T / delta) + 1
    steps = np.linspace(0.0, T, count)

    u     = np.zeros(count)
    h     = np.zeros(count)

    for n in xrange(count - 1):
        if n * delta < 5.0:
            m_p_dot = 20.0
            m_p     = m_po - (m_p_dot * n * delta)
        else:
            m_p_dot = 0.0
            m_p     = 0.0

        h_n = u[n]
        v_n = -g + ((m_p_dot * v_e) - (0.5 * rho * u[n] * np.abs(u[n]) * A * C_d)) / (m_s + m_p)

        h[n + 1] = h[n] + delta * h_n
        u[n + 1] = u[n] + delta * v_n

    results  = np.column_stack((steps, h, u))

    altitude = results[:, 1]
    velocity = results[:, 2]

    index1   = np.argmax(velocity)
    index2   = np.argmax(altitude)
    index3   = np.where(altitude < 0.0)[0][0]

    print_results(results, index1, index2, index3)

    plot_single(steps, altitude, ['Altitude'], 'rocket_altitude_01.png')
    plot_single(steps, velocity, ['Velocity'], 'rocket_velocity_01.png')


if __name__ == "__main__":
    main(sys.argv[1:])