import numpy as np

## written by Dennis van Dommelen, 2014

def gust1(t):
    ## syntax: gust1(t)
    ## 'smooth' wind gust
    ##
    ## Output:
    ##    U: wind speed [m/s]; with respect to mean wind speed V
    ## Input:
    ##    t: time [s]

    ## gust amplitude
    A=1
    ## gust duration
    T=12
    ## starting time of gust
    t0=5

    
    ## all values of U before or after the gust are put to zero
    if (t<t0 or t>t0+T):
        U=0
    ## gust
    else:
        U=0.5*A*(1-np.cos(2*np.pi*(t-t0)/T))
    

    

    return U
