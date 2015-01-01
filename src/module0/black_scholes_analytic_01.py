import sys
import math




def d1(S, K, sigma, r, t):
    return (math.log(S / K) + (r + (sigma ** 2) / 2.0) * t) / (sigma * math.sqrt(t))

def d2(S, K, sigma, r, t):
    return d1(S, K, sigma, r, t) - sigma * math.sqrt(t)




def call(S, K, sigma, r, t):
    return (S * cnorm(d1(S, K, sigma, r, t))) - (K * cnorm(d2(S, K, sigma, r, t)) * math.exp(-r * t))

def put(S, K, sigma, r, t):
    return (K * cnorm(-d2(S, K, sigma, r, t)) * math.exp(-r * t)) - (S * cnorm(-d1(S, K, sigma, r, t)))




def cnorm(x):
    if x >= 0:
        b0 =  0.2316419
        b1 =  0.319381530
        b2 = -0.356563782
        b3 =  1.781477937
        b4 = -1.821255978
        b5 =  1.330274429

        N  = math.exp(-(x ** 2) / 2.0) / math.sqrt(2 * math.pi)
        t  = 1.0 / (1.0 + b0 * x)

        return 1 - N * (b1 * t + b2 * (t ** 2) + b3 * math.pow(t, 3) + b4 * math.pow(t, 4) + b5 * math.pow(t, 5))
    else:
        return 1 - cnorm(-x)




def pcp_put(S, K, r, t, c):
    return c + (K * math.exp(-r * t) - S)

def pcp_call(S, K, r, t, p):
    return p - (K * math.exp(-r * t) - S)



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
