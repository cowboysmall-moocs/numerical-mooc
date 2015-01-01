import sys

import numpy as np

from scipy.linalg import solve




def computeAlpha(dt, J, r, sigma):
    return 0.5 * dt * ((r * J) - ((sigma ** 2) * (J ** 2)))


def computeBeta(dt, J, r, sigma):
    return 1 + (((sigma ** 2) * (J ** 2) + r) * dt)


def computeGamma(dt, J, r, sigma):
    return -0.5 * dt * ((r * J) + ((sigma ** 2) * (J ** 2)))





def generateMatrix(M, dt, r, sigma):
    d  = np.diag(computeBeta(dt, np.arange(1, M - 1), r, sigma))
    ud = np.diag(computeGamma(dt, np.arange(1, M - 2), r, sigma), 1)
    ld = np.diag(computeAlpha(dt, np.arange(2, M - 1), r, sigma), -1)
    return d + ud + ld


def generateRHS(option, M, dt, r, sigma):
    b      = option[1:-2]
    b[0]  -= option[0] * computeAlpha(dt, 1, r, sigma)
    b[-1] -= option[-1] * computeGamma(dt, M - 1, r, sigma)
    return b


def generatePut(M, ds, K):
    put      = np.ones(M + 1) * K - np.arange(M + 1) * ds
    neg      = np.where(put < 0.0)[0]
    put[neg] = 0
    return put





def implicit(A, option, M, N, dt, r, K, sigma):
    sol       = np.zeros((M + 1, N + 1))
    sol[:, 0] = option.copy()

    for t in xrange(1, N + 1):
        b            = generateRHS(option, M, dt, r, sigma)
        s            = solve(A, b)

        option[1:-2] = s.copy()
        option[0]    = K * np.exp(-r * (N - t) * dt)
        option[-1]   = 0

        sol[:, t]    = option.copy()

    return sol





def main(argv):
    S     = 500.0
    T     =   3.0

    M     = 1000
    N     = 1000

    ds    = S / M
    dt    = T / N

    sigma =  0.25
    r     =  0.05
    K     = 50.00

    A     = generateMatrix(M, dt, r, sigma)
    put   = generatePut(M, ds, K)
    sol   = implicit(A, put, M, N, dt, r, K, sigma)

    print 
    print 'Numerical Solutions For Black Scholes (implicit)'
    print 
    print 'S[%s]: %10.4f' % (10, sol[int(10.0 / ds), -1])
    print 'S[%s]: %10.4f' % (15, sol[int(15.0 / ds), -1])
    print 'S[%s]: %10.4f' % (20, sol[int(20.0 / ds), -1])
    print 'S[%s]: %10.4f' % (25, sol[int(25.0 / ds), -1])
    print 'S[%s]: %10.4f' % (30, sol[int(30.0 / ds), -1])
    print 'S[%s]: %10.4f' % (35, sol[int(35.0 / ds), -1])
    print 'S[%s]: %10.4f' % (40, sol[int(40.0 / ds), -1])
    print 'S[%s]: %10.4f' % (45, sol[int(45.0 / ds), -1])
    print 'S[%s]: %10.4f' % (50, sol[int(50.0 / ds), -1])
    print 'S[%s]: %10.4f' % (55, sol[int(55.0 / ds), -1])
    print 'S[%s]: %10.4f' % (60, sol[int(60.0 / ds), -1])
    print 'S[%s]: %10.4f' % (65, sol[int(65.0 / ds), -1])
    print 'S[%s]: %10.4f' % (70, sol[int(70.0 / ds), -1])
    print 'S[%s]: %10.4f' % (75, sol[int(75.0 / ds), -1])
    print 'S[%s]: %10.4f' % (80, sol[int(80.0 / ds), -1])
    print 'S[%s]: %10.4f' % (85, sol[int(85.0 / ds), -1])
    print 'S[%s]: %10.4f' % (90, sol[int(90.0 / ds), -1])
    print 



if __name__ == "__main__":
    main(sys.argv[1:])
