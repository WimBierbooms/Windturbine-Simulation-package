import numpy as np

## written by Dennis van Dommelen, 2014

def gust2(t,omr):
    ## syntax: gust2(t,omr)
    ## Wind gust with the shape of a sine; the frequency equals the rotor angular velocity (1P). This gust
    ## represents the variations in the wind speed at a blade section due to wind shear, yawed flow,
    ## tower shadow and rotational sampling of turbulence.
    ## Note: the amplitude of this gust will depend on the radial position of the blade section; for the sake
    ##       of simplicity it is here assumed that the amplitude is equal for all blade sections
    ##
    ## Output:
    ##    U: wind speed [m/s]; with respect to the mean wind speed V
    ## Inputs:
    ##    t: time [s]
    ##    omr: rotor angular velocity [rad/s]

    ## gust amplitude
    A=1

    ## gust
    U=A*np.sin(omr*t)
    return U
