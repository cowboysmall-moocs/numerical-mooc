import sys

import numpy as np

from euler import euler_step, numerical_solution, get_error
from plot import plot_single, plot_multiple, plot_error



def fugoid_numerical(u, time, zt = 100., z0 = 100., v = 10., g = 9.81):
    return np.array([u[1], g * (1 - u[0] / zt)])



def fugoid_analytic(steps, zt = 100., z0 = 100., v = 10., g = 9.81):
    return v * ((zt / g) ** 0.5 * np.sin((g / zt) ** 0.5 * steps)) + ((z0 - zt) * np.cos((g / zt) ** 0.5 * steps)) + zt



def main(argv):
    numerical_result  = numerical_solution(100.0, 0.01, fugoid_numerical, [100., 10.])
    analytical_result = fugoid_analytic(numerical_result[:, 0])

    plot_multiple(numerical_result[:, 0], [numerical_result[:, 1], analytical_result], ['Numerical', 'Analytical'], 'phugoid_trajectory.png')

    deltas = np.array([0.1, 0.05, 0.01, 0.005, 0.001, 0.0001])
    errors = np.empty_like(deltas)

    for i, delta in enumerate(deltas):
        numerical  = numerical_solution(100.0, delta, fugoid_numerical, [100., 10.])
        analytical = fugoid_analytic(numerical[:, 0])
        errors[i]  = get_error(numerical[:, 1], analytical, delta)

    plot_error(deltas, errors, 'phugoid_errors.png')



if __name__ == "__main__":
    main(sys.argv[1:])
