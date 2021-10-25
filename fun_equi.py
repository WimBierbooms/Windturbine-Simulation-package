from bem import bem
from gen import gen

## written by Dennis van Dommelen, 2014

def fun_equi(omr,V,theta,windturbine):
    ## syntax: fun_equi(omr,V,theta,windturbine)
    ## Determination of difference between aerodynamic rotor torque and generator torque,
    ## for known rotor angular velocity
    ## This function is used by 'equi.py'
    ##
    ## Output:
    ##    Md: difference in torque [Nm]
    ## Inputs:
    ##    omr: rotor angular velocity [rad/s]
    ##    V: undisturbed wind speed [m/s]
    ##    theta: pitch angle [degrees]
    ##    windturbine: name of the windturbine file consisting of the windturbine parameters
    ##          e.g. 'V90'
    

    ##Required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())

    ##    P1: aerodynamic parameters
    ##    P2: turbine parameters
    ##    P3: blade geometry
    ##    P4: nominal values

    ## transmission ratio [-]
    nu=P2[7]

    ## stationary conditions: flap velocity and tower top velocity are equal zero
    betad=0
    xd=0

    ## aerodynamic rotor torque Mr according to blade element-momentum methode (BEM) for known rotor angular velocity
    [Dax,Mbeta,Mr,P,Cdax,Cp,a]=bem(V,theta,betad,omr,xd,windturbine)

    ## stationary generator angular velocity (for known rotor angular velocity)
    omg=nu*omr
    ## generator torque
    [Mg,Pg]=gen(omg,windturbine)

    ## generator torque, with respect to the low speed shaft
    Mg2=nu*Mg;
    ## difference in torque (with respect to the low speed shaft)
    Md=Mr-Mg2;

    return Md
