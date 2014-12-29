import sys
import math




def d1(S, K, sigma, r, t):
    v1 = math.log(S / K)
    v2 = (r + ((sigma ** 2) / 2.0)) * t
    v3 = sigma * math.sqrt(t)
    return (v1 + v2) / v3

def d2(S, K, sigma, r, t):
    return d1(S, K, sigma, r, t) - sigma * math.sqrt(t)




def call(S, K, sigma, r, t):
    v1 = d1(S, K, sigma, r, t)
    v2 = d2(S, K, sigma, r, t)
    return (S * error_function(v1)) - (K * error_function(v2) / math.exp(r * t))

def put(S, K, sigma, r, t):
    v1 = d1(S, K, sigma, r, t)
    v2 = d2(S, K, sigma, r, t)
    return (K * error_function(-v2) / math.exp(r * t)) - (S * error_function(-v1))




def error_function(x):
    gamma = 0.2316419
    k     = 1.0 / (1.0 + x * gamma)

    a1    =  0.319381530
    a2    = -0.356563782
    a3    =  1.781477937
    a4    = -1.821255978
    a5    =  1.330274429

    q     = 1.0 / math.sqrt(2 * math.pi)
    N     = q / math.exp((x ** 2) / 2.0)

    if x >= 0:
        return 1 - N * (a1 * k + a2 * math.pow(k, 2) + a3 * math.pow(k, 3) + a4 * math.pow(k, 4) + a5 * math.pow(k, 5))
    else:
        return 1 - error_function(-x)




def put_call_put(S, K, r, t, c):
    return K / math.exp(r * t) + c - S

def put_call_call(S, K, r, t, p):
    return S + p - K / math.exp(r * t)



def main(argv):
    print 
    print 'Analytic Solutions For Black Scholes'
    print 
    print 'S[%s]: %10.4f' % (10, put(10, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (15, put(15, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (20, put(20, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (25, put(25, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (30, put(30, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (35, put(35, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (40, put(40, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (45, put(45, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (50, put(50, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (55, put(55, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (60, put(60, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (65, put(65, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (70, put(70, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (75, put(75, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (80, put(80, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (85, put(85, 50.0, 0.25, 0.05, 3))
    print 'S[%s]: %10.4f' % (90, put(90, 50.0, 0.25, 0.05, 3))
    print 



if __name__ == "__main__":
    main(sys.argv[1:])
