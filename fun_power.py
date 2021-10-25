from bem import bem

## written by Dennis van Dommelen, 2014

def fun_power(theta,V,Pn,windturbine):
    ## syntax: power2(theta,V,Pn,windturbine())
    ## Determination of difference between aerodynamic power, for known blade pitch angle, 
    ## and nominal power
    ## This function is used by 'powercurve1.py' and 'equi.py'
    ##
    ## Output:
    ##    Pd: difference in power [W]
    ## Input:
    ##    theta: blade pitch anlge [degrees]
    ##    V: undisturbed wind speed [m/s]
    ##    Pn: nominal mechanical power [W]
    ##    windturbine: name of file with wind turbine parameters
    ##                 e.g.: 'LW50'


    ## required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ##    P1: aerodynamic parameters
    ##    P2: turbine parameters
    ##    P3: blade geometry
    ##    P4: nominal values

    
    ## rotor radius
    R=P2[0]
    ## nominal wind speed [m/s]
    Vn=P4[0]
    ## nominal tip speed ratio [-]
    lambdan=P4[1]

    ## stationary conditions: flap velocity and tower top velocity are equal zero
    betad=0.
    xd=0.

    ## the rotor angular velocity is kept constant at nominal value
    omr=lambdan*Vn/R

    ## power according to blade element-momentum method (BEM) for known blade pitch angle
    [Dax,Mbeta,Mr,P,Cdax,Cp,a]=bem(V,theta,betad,omr,xd,windturbine)

    ## difference in power
    Pd=P-Pn

    return Pd
