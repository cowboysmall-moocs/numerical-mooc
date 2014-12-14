import numpy as np


def numerical_solution(duration, delta, f, initial, **params):
    count = int(duration / delta) + 1
    steps = np.linspace(0.0, duration, count)

    u     = np.empty((count, len(initial)))
    u[0]  = np.array(initial)

    for n in xrange(count - 1):
        u[n + 1] = euler_step(u[n], delta, f, n * delta, **params)

    return np.column_stack((steps, u))



def euler_step(u, delta, f, time, **params):
    return u + delta * f(u, time, **params)



def get_error(numeric, analytic, delta):
    return delta * np.sum(np.abs(numeric - analytic))
