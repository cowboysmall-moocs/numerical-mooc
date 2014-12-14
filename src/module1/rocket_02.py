import sys

import numpy as np
import matplotlib.pyplot as plt

from euler import euler_step, numerical_solution



def rocket_numerical(u, time, m_s = 50.0, rho = 1.091, r = 0.5, g = 9.81, v_e = 325.0, C_d = 0.15, m_po = 100.0):
    A = np.pi * (r ** 2.0)
    if time < 5.0:
        m_p_dot = 20.0
        m_p     = m_po - (m_p_dot * time)
    else:
        m_p_dot = 0.0
        m_p     = 0.0
    v = -g + ((m_p_dot * v_e) - (0.5 * rho * u[0] * np.abs(u[0]) * A * C_d)) / (m_s + m_p)
    h = u[0]
    return np.array([v, h])



def print_results(results, index1, index2, index3):
    print 
    print ' maximum velocity: %0.2f' % (results[index1, 1])
    print '             time: %0.2f' % (results[index1, 0])
    print '         altitude: %0.2f' % (results[index1, 2])
    print 
    print '   maximum height: %0.2f' % (results[index2, 2])
    print '             time: %0.2f' % (results[index2, 0])
    print 
    print '   time of impact: %0.2f' % (results[index3, 0])
    print '         velocity: %0.2f' % (results[index3, 1])
    print



def main(argv):
    numerical_result = numerical_solution(40.0, 0.1, rocket_numerical, [0., 0.])

    velocity = numerical_result[:, 1]
    altitude = numerical_result[:, 2]

    idx_1    = np.argmax(velocity)
    idx_2    = np.argmax(altitude)
    idx_3    = np.where(altitude < 0.0)[0][0]

    print_results(numerical_result, idx_1, idx_2, idx_3)

    # plot_single(steps, altitude, ['Altitude'])
    # plot_single(steps, velocity, ['Velocity'])


if __name__ == "__main__":
    main(sys.argv[1:])
