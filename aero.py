import numpy as np
import math
from lift import lift
from drag import drag

## written by Dennis van Dommelen, 2014

def aero(a,V,theta,betad,omr,xd,windturbine):

    ## syntax: aero(a,V,theta,betad,omr,xd,windturbine);
    ## Determination of the aerodynamic forces, moments and power by means of
    ## the blade element method; for known mean wind speed, induction factor etc.
    ## Simplifications:
    ##    - uniform flow (i.e. wind speed constant over rotor plane; no yawed flow, windshear or tower shadow)
    ##    - no wake rotation (i.e. no tangential induction factor)
    ##    - no blade tip loss factor
    ##
    ## Output:
    ##    Dax: axial force [N]
    ##    Mbeta: aerodynamic flap moment [Nm]
    ##    Mr: aerodynamic rotor torque [Nm]
    ##    P: aerodynamic power [W]
    ##    Cdax: thrust coefficient [-]
    ##    Cp: power coefficient [-]
    ## Input:
    ##    a: induction factor [-]
    ##    V: undisturbed wind speed [m/s]
    ##    theta: pitch angle [degrees]
    ##    betad: flap velocity [rad/s]
    ##    omr: rotor angular velocity [rad/s]
    ##    xd: tower top velocity [m/s]
    ##    windturbine (e.g. 'V90') gives all parameters of the windturbine


    ##    Required parameters    
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ##    P1: aerodynamic parameters
    ##    P2: turbine parameters
    ##    P3: blade geometry
    
    dDax = []
    dMbeta = []
    dMr = []
    ## air density [kg/m3]
    rho=P1[0]
    ## power loss factor; correction factor for the above mentioned simplifications [-]
    kp=P1[1]
    ## rotor radius [m]
    R=P2[0]
    ## number of blades [-]
    Nb=P2[1]
    ## number of blade elements [-]
    Ns=len(P3[0])-1
    ## radial position blade elements [m]
    r=P3[0]
    ## chord blade elements [m]
    c=P3[1]
    ## twist blade elements [degrees];
    thetat=P3[2]

    ## calculation of aerodynamic forces/moments for each blade section
    for i in range(0,Ns):
       ## use mean value for the radial position of blade element
       ri=(r[i]+r[i+1])/2
       ## idem chord
       ci=(c[i]+c[i+1])/2
       ## idem twist
       thetati=(thetat[i]+thetat[i+1])/2
       ## length blade element
       dr=r[i+1]-r[i]
       ## perpendicular velocity component
       Vp=V*(1-a)-betad*ri-xd
       ## tangential velocity component
       Vt=omr*ri
       ## resultant velocity
       W=np.sqrt(Vp**2+Vt**2)
       ## angle of inflow
       phi=math.atan(Vp/Vt)
       ## angle of attack (in degrees)
       alpha=180./np.pi*phi-(theta+thetati)
       ## lift coefficient (from function 'lift.m')
       Cl=lift(alpha)
       ## lift force blade element
       dL=Cl*0.5*rho*W**2*ci*dr
       ## drag coefficient (from function 'drag.m')
       Cd=drag(alpha)
       ## drag force blade element
       dD=Cd*0.5*rho*W**2*ci*dr
       ## contribution to axial force
       dDax.append(Nb*(dL*np.cos(phi)+dD*np.sin(phi)))
       ## contribution to aerodynamic flap moment
       dMbeta.append(ri*(dL*np.cos(phi)+dD*np.sin(phi)))
       ## contribution to aerodynamic rotor torque
       dMr.append(Nb*ri*(kp*dL*np.sin(phi)-dD*np.cos(phi)))
    

    ## total forces and moments; sommation over all blade elements
    Dax=sum(dDax)
    Mbeta=sum(dMbeta)
    Mr=sum(dMr)

    ## thrust coefficient
    Cdax=Dax/(0.5*rho*np.pi*R**2*V**2)

    ## aerodynamic power
    P=omr*Mr

    ## power coefficient
    Cp=P/(0.5*rho*np.pi*R**2*V**3)
    return Dax,Mbeta,Mr,P,Cdax,Cp
