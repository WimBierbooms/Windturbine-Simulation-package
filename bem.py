from aero import aero
from scipy.optimize import fsolve
from fun_bem import fun_bem
import math
from scipy.optimize import fsolve

## written by Dennis van Dommelen, 2014

def bem(V,theta,betad,omr,xd,windturbine):
    ## syntax: bem(V,theta,betad,omr,xd,windturbine)
    ## Determintion of the aerodynamic forces, moments and power by means of the
    ## blade element - momentum method (BEM); for known wind speed, pitch angle, etc.
    ## Simplifications:
    ##    - uniform flow (i.e. wind speed constant over rotor plane; no yawed flow, windshear or tower shadow)
    ##    - no wake rotation (i.e. no tangential induction factor)
    ##    - no blade tip loss factor
    ##    - just one annular section (the total rotor plane)
    ##
    ## Output:
    ##    Dax: axial force [N]
    ##    Mbeta: aerodynamic flap moment [Nm]
    ##    Mr: aerodynamic rotor torque [Nm]
    ##    P: aerodynamic power [W]
    ##    Cdax: thrust coefficient [-]
    ##    Cp: power coefficient [-]
    ##    a: induction factor [-]
    ## Input:
    ##    V: undisturbed wind speed [m/s]
    ##    theta: pitch angle [degrees]
    ##    betad: flap velocity [rad/s]
    ##    omr: rotor angular velocity [rad/s]
    ##    xd: tower top velocity [m/s]
    ##    windturbine name of file with wind turbine parameters
    ##                 e.g.: 'LW50'

    ##    required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ##    P1: aerodynamic parameters
    ##    P2: turbine parameters
    ##    P3: blade geometry

    
    ## Calculation of the inductionfactor a by means of BEM:
    ## Cdax according to the blade element method should be equal to Cdax according to the momentum theory
    ## Use is made of the standard Python.scipy.optimize routine 'fsolve' to find a zero of the function 'fun_bem.py'; 'fsolve' varies
    ## the induction factor a (starting value 0.5) until 'fun_bem' equals (about) zero.
    
    a=fsolve(fun_bem,0.5,args=(V,theta,betad,omr,xd,windturbine))[0]
   

    ## since the induction factor is determined, the aerodynamic forces, moments and power
    ## can be calculated by means of the blade element method
    [Dax,Mbeta,Mr,P,Cdax,Cp]=aero(a,V,theta,betad,omr,xd,windturbine);
    return Dax,Mbeta,Mr,P,Cdax,Cp,a
