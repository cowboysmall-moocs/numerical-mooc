import sys

import sympy
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation



def solve_eq(rho_m, u_m, u_s):
    u_max, u_star, rho_max, rho_star, A, B = sympy.symbols('u_max u_star rho_max rho_star A B')

    eq1     = sympy.Eq( 0, u_max * rho_max * (1 - A * rho_max - B * rho_max ** 2) )
    eq2     = sympy.Eq( 0, u_max * (1 - 2 * A * rho_star - 3 * B * rho_star ** 2) )
    eq3     = sympy.Eq( u_star, u_max * (1 - A * rho_star - B * rho_star ** 2) )

    eq4     = sympy.Eq( eq2.lhs - 3 * eq3.lhs, eq2.rhs - 3 * eq3.rhs )
    eq4.simplify()
    eq4.expand()

    rho_sol = sympy.solve(eq4, rho_star)[0]
    B_sol   = sympy.solve(eq1, B)[0]

    quadA   = eq2.subs([(rho_star, rho_sol), (B, B_sol)])
    quadA.simplify()

    A_sol   = sympy.solve(quadA, A)[0]

    aval    = A_sol.evalf( subs = {u_star: u_s, u_max: u_m, rho_max: rho_m} )
    bval    = B_sol.evalf( subs = {rho_max: rho_m, A: aval} )

    rho_sol = sympy.solve(eq2, rho_star)[0]
    rho_val = rho_sol.evalf( subs = {u_max: u_m, A: aval, B: bval} )

    return aval, bval, rho_val


def computeF(u_max, rho, aval, bval):
    return u_max * rho * (1 - (aval * rho) - (bval * (rho ** 2)))


def rho_green_light(nx, rho_light):
    rho_initial = np.arange(nx) * 2.0 / nx * rho_light
    rho_initial[(nx - 1) / 2:] = 0
    return rho_initial


def ftbs(rho, nt, dt, dx, rho_max, u_max, aval, bval):
    rho_n       = np.zeros((nt, len(rho))) 
    rho_n[0, :] = rho.copy()              
    
    for t in xrange(1, nt):
        F            = computeF(u_max, rho, aval, bval)
        rho_n[t, 1:] = rho[1:] - (dt / dx) * (F[1:] - F[:-1])
        rho_n[t, 0]  = rho[0]
        rho_n[t, -1] = rho[-1]
        rho          = rho_n[t].copy()

    return rho_n



def plot(x, rho, filename):
    plt.clf()
    plt.plot(x, rho, color = '#003366', ls = '-', lw = 3)
    plt.ylabel('Traffic density')
    plt.xlabel('Distance')
    plt.ylim(-0.5, 11.0)
    plt.savefig('./src/module3/images/' + filename, format = 'png')
    plt.close()


def main(argv):
    sigma     = 1.0
    nx        = 81
    nt        = 30
    dx        = 4.0 / (nx - 1)

    x         = np.linspace(0, 4, nx)

    rho_light = 5.5
    rho_max   = 10.0
    u_max     = 1.0
    u_star    = 0.7

    dt        = sigma * dx / u_max

    rho_initial = rho_green_light(nx, rho_light)
    plot(x, rho_initial, 'traffic_03.png')

    aval, bval, rho_val = solve_eq(rho_max, u_max, u_star)
    rho_n               = ftbs(rho_initial, nt, dt, dx, rho_max, u_max, aval, bval)

    def animate(data):
        x = np.linspace(0, 4, nx)
        y = data
        line.set_data(x, y)
        return line

    fig   = plt.figure(facecolor = 'w')
    ax    = plt.axes(xlim = (0, 4), ylim = (-1, 8), xlabel = ('Distance'), ylabel = ('Traffic density'))
    line, = ax.plot([],[], color = '#003366', lw = 2)
    anim  = animation.FuncAnimation(fig, animate, frames = rho_n, interval = 50)
    plt.show()



if __name__ == "__main__":
    main(sys.argv[1:])
