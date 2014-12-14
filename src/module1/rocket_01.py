import sys

import numpy as np
import matplotlib.pyplot as plt

from plot import plot_single, plot_multiple, plot_error


def main(argv):
    T     = 40.0
    delta = 0.1

    m_s   = 50.0
    rho   = 1.091
    A     = np.pi * (0.5 ** 2.0)
    g     = 9.81
    v_e   = 325.0
    C_d   = 0.15
    m_po  = 100.0

    count = int(T / delta) + 1
    steps = np.linspace(0.0, T, count)

    u     = np.zeros(count)
    h     = np.zeros(count)

    for n in xrange(count - 1):
        if n * delta < 5.0:
            m_pdot = 20.0
            m_p    = m_po - (m_pdot * n * delta)
        else:
            m_pdot = 0.0
            m_p    = 0.0

        u[n + 1] = u[n] + delta * (-g + ((m_pdot * v_e) - (0.5 * rho * u[n] * np.abs(u[n]) * A * C_d)) / (m_s + m_p))
        h[n + 1] = h[n] + delta * u[n]

    numerical_result = np.column_stack((steps, h, u))

    altitude = numerical_result[:, 1]
    velocity = numerical_result[:, 2]

    idx_1 = np.argmax(velocity)
    idx_2 = np.argmax(altitude)
    idx_3 = np.where(altitude < 0.0)[0][0]

    print
    print numerical_result[0:11, ]
    print 
    print ' maximum velocity: %0.2f' % (numerical_result[idx_1, 2])
    print '             time: %0.2f' % (numerical_result[idx_1, 0])
    print '         altitude: %0.2f' % (numerical_result[idx_1, 1])
    print 
    print '   maximum height: %0.2f' % (numerical_result[idx_2, 1])
    print '             time: %0.2f' % (numerical_result[idx_2, 0])
    print 
    print '   time of impact: %0.2f' % (numerical_result[idx_3, 0])
    print '         velocity: %0.2f' % (numerical_result[idx_3, 2])
    print

    # plot_single(steps, altitude, ['Altitude'])
    # plot_single(steps, velocity, ['Velocity'])



if __name__ == "__main__":
    main(sys.argv[1:])
