import sys

import numpy as np
import matplotlib.pyplot as plt

from euler import euler_step, numerical_solution, get_error
from plot import plot_single, plot_multiple, plot_error



def fugoid_numerical(u, time, **params):
    return np.array([u[1], params['g'] * (1 - u[0] / params['zt'])])



def fugoid_analytic(steps, **params):
    A = (params['zt'] / params['g']) ** 0.5 * np.sin((params['g'] / params['zt']) ** 0.5 * steps)
    B = (params['z0'] - params['zt']) * np.cos((params['g'] / params['zt']) ** 0.5 * steps)
    return params['v'] * A + B + params['zt']



def main(argv):
    params = { 'zt': 100., 'z0': 100., 'v': 10, 'g': 9.81 }


    numerical_result = numerical_solution(100.0, 0.01, fugoid_numerical, [100., 10], **params)
    analytic_result  = fugoid_analytic(numerical_result[:, 0], **params)

    plot_multiple(numerical_result[:, 0], [numerical_result[:, 1], analytic_result], ['Numerical Solution', 'Analytical Solution'])


    deltas = np.array([0.1, 0.05, 0.01, 0.005, 0.001, 0.0001])
    errors = np.empty_like(deltas)
    for i, delta in enumerate(deltas):
        numerical = numerical_solution(100.0, delta, fugoid_numerical, [100., 10], **params)
        analytic  = fugoid_analytic(numerical[:, 0], **params)
        errors[i] = get_error(numerical[:, 1], analytic, delta)

    plot_error(deltas, errors)



if __name__ == "__main__":
    main(sys.argv[1:])
