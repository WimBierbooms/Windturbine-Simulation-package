import math
from bem import bem
from fun_equi import fun_equi
from fun_power import fun_power
from scipy.optimize import fsolve

## written by Dennis van Dommelen, 2014

def equi(windturbine,V):
    ## syntax: equi(windturbine,V)
    ## Determination of the operating point of the wind turbine for known wind speed;
    ## this is the steady state after equilibrium between all acting forces on the wind turbine
    ##
    ##    Partial load conditions (V<=Vn): theta=thetan.
    ##        Note: it is not assumed that the wind turbine automatically operates at optimal tip speed ratio
    ##    Full load conditions (V>Vn): omr=omrn; theta such that power equals nominal power
    ##
    ## Inputs:
    ##    windturbine: name of file with wind turbine parameters
    ##                 e.g.: 'LW50'
    ##    V: undisturbed wind speed [m/s]
    ## Outputs:
    ##    beta0: stationary flap angle [rad]
    ##    x0: stationary tower top displacement [m]
    ##    omr0: stationary rotor angular velocity [rad/s]
    ##    eps0: stationary torsion angle transmission [rad]
    ##    omg0; stationary generator angular velocity [rad/s]
    ##    a0: stationary induction factor [-]
    ##    theta: blade pitch angle [degrees]
    ##    Dax0: stationary axial force [N]
    ##    Mbeta0: stationary aerodynamic flap moment [Nm]
    ##    Mr0: stationary aerodynamic rotor torque [Nm]

    ## required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ## rotor radius [m]
    R=P2[0]
    ## inertia blade (with respect to flapping hinge) [kg m^2]
    Jb=P2[2]
    ## stifness flap spring [Nm/rad]
    kb=P2[3]
    ## stifness tower [N/m]
    kt=P2[6]
    ## transmission ratio [-]
    nu=P2[7]
    ## stiffness transmission [Nm/rad]
    kr=P2[10]
    ## nominal wind speed [m/s]
    Vn=P4[0]
    ## nominal tip speed ratio [-]
    lambdan=P4[1]
    ## nominal blade pitch angle [degrees]
    thetan=P4[2]

    ## stationary conditions: flap velocity and tower top velocity are equal zero
    betad=0
    xd=0

    ## nominal rotor angular velocity
    omrn=lambdan*Vn/R
    ## nominal mechanical power Pn (wind speed equal to nominal wind speed; blade pitch angle equal to
    ##                    nominal blade pitch angle; rotor angular velocity equal to nominal rotor angular velocity)
    [Dax,Mbeta,Mr,Pn,Cdax,Cp,a]=bem(Vn,thetan,betad,omrn,xd,windturbine)

    if (V <= Vn):
        ## partial load conditions (wind speed smaller or equal nominal wind speed)
        ## blade pitch angle equals nominal blade pitch angle
        theta=thetan
        ## operating point: equilibrium between aerodynamic rotor torque and generator torque
        ## Use is made of the standard Python.scipy.optimize routine 'fsolve' to find a zero of the function 'fun_bem.py'; 'fzero' varies
        ## the rotor angular velocity (with starting value 7.5*V/R; corresponding with a tip speed ratio of 7.5)
        ## until 'fun_equi' equals (about) zero.
        
       
        omr0=fsolve(fun_equi,7.5*V/R,args=(V,theta,windturbine))[0]
        
        
    else:
        ## ful load conditions (wind speed larger than nominal wind speed)
        ## rotor angular velocity equals nominal rotor angular velocity
        omr0=lambdan*Vn/R
        ## the blade pitch angle should be such that the power equals nominal power;
        ## it is assumed that the blade pitch control is to zero-lift
        ## Use is made of the standard Python.scipy.optimize routine 'fsolve' to find a zero of the function 'fun_power.py'; 'fsolve' varies
        ## the blade pitch angle (with starting value 25) until 'fun_power' equals (about) zero.
        theta=fsolve(fun_power,25.,args=(V,Pn,windturbine))[0]
        

    ## since the blade pitch angle and the stationary rotor angular velocity are determined, the stationary
    ## aerodynamic forces, moments and induction factor can be calculated by means of
    ## the blade element - momentum method (BEM)
    [Dax0,Mbeta0,Mr0,P,Cdax,Cp,a0]=bem(V,theta,betad,omr0,xd,windturbine)

    ## equilibrium equations of the turbine: the equations of motion (see listing 'dynmod.m')
    ## without time dependent terms
    ## stationary flap angle
    beta0=Mbeta0/(kb+Jb*omr0**2)
    ## stationary tower top displacement
    x0=Dax0/kt
    ## stationary torsion angle transmission
    eps0=Mr0/kr
    ## stationary generator angular velocity
    omg0=nu*omr0

    return [beta0,x0,omr0,eps0,omg0,a0,theta,Dax0,Mbeta0,Mr0]
