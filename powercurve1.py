from bem import bem
from fun_power import fun_power
from scipy.optimize import fsolve

## written by Dennis van Dommelen, 2014

def powercurve1(windturbine,V):
    ## syntax: powercurve1(windturbine,V)
    ## Determination of the characteristics of a VARIABLE SPEED REGULATED wind turbine
    ##    axial force versus wind speed                  Dax - V
    ##    aerodynamic flap moment versus wind speed      Mbeta - V
    ##    aerodynamic rotor torque versus wind speed     Mr - V
    ##    aerodynamic power versus wind speed            P - V
    ##    thrust coefficient versus wind speed           Cdax - V
    ##    power coefficient versus wind speed            Cp - V
    ##    induction factor versus wind speed             a - V
    ##    blade pitch angle versus wind speed            theta - V
    ##    rotor angular velocity versus wind speed       omr - V
    ## It is assumed that the wind turbine has an optimal lambda control, so:
    ##    Partial load (V<=Vn): lambda=lambdan, theta=thetan
    ##    Full load (V>Vn): omr=omrn; theta such that power equals nominal power
    ##
    ## Outputs:
    ##    Dax: axial force [N]
    ##    Mbeta: aerodynamic flap moment [Nm]
    ##    Mr: aerodynamic rotor torque [Nm]
    ##    P: aerodynamic power [W]
    ##    Cdax: thrust coefficient [-]
    ##    Cp: power coefficient [-]
    ##    a: induction factor [-]
    ##    theta: blade pitch angle [degrees]
    ##    omr: rotor angular velocity [rad/s]
    ## Inputs:
    ##    windturbine: name of file with wind turbine parameters (string)
    ##                 e.g.: 'LW50'
    ##    V: vector with wind speeds [m/s]

    ## required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ## rotor radius
    R=P2[0]
    ## transmission ratio [-]
    nu=P2[7]
    ## nominal wind speed [m/s]
    Vn=P4[0]
    ## nominal tip speed ratio [-]
    lambdan=P4[1]
    ## nominal blade pitch angle [degrees]
    thetan=P4[2]

    ## stationary conditions: flap speed and tower top speed equal zero
    betad=0
    xd=0

    ## nominal rotor angular velocity
    omrn=lambdan*Vn/R
    ## nominal (mechanical) generator angular velocity 
    omgn=nu*omrn
    ## nominal mechanical power Pn (wind speed equal to nominal wind speed; blade pitch angle equal to
    ##              nominal blade pitch angle; rotor angular velocity equal to nominal rotor angular velocity)
    [Dax,Mbeta,Mr,Pn,Cdax,Cp,a]=bem(Vn,thetan,betad,omrn,xd,windturbine)

    N=len(V)

    Dax_list = []
    Mbeta_list = []
    Mr_list = []
    P_list = []
    Cdax_list = []
    Cp_list = []
    a_list = []
    theta_list = []
    omr_list = []
    ## calculation of aerodynamic forces, moments etc. for each wind speed
    for i in range(N):
      if V[i] <= Vn:
         ## partial load conditions (wind speed smaller or equal nominal wind speed)
         ## the tip speed ratio equals nominal tip speed ratio, so the rotor angular velocity equals:
         omri=lambdan*V[i]/R
         ## the blade pitch angle equals nominal blade pitch angle
         thetai=thetan
         ## calculation of the aerodynamic forces, moments etc. by means of blade element-momentum method (BEM)
         [Daxi,Mbetai,Mri,Pi,Cdaxi,Cpi,ai]=bem(V[i],thetai,betad,omri,xd,windturbine)
      else:
         ## full load conditions (wind speed larger than nominal wind speed)
         ## the rotor angular velocity is kept constant at nominal value
         omri=lambdan*Vn/R
         ## the blade pitch angle should be such that the power equals nominal power;
         ## it is assumed that the blade pitch control is to zero-lift
         ## Use is made of the standard Python.scipy.optimize routine 'fsolve' to find a zero of the function 'fun_power.py'; 'fzero' varies
         ## the blade pitch angle (with starting value 25) until 'fun_power.py' equals (about) zero.
   
         thetai=fsolve(fun_power,25,args=(V[i],Pn,windturbine))[0]
         
         ## since the blade pitch angle is determined, the aerodynamic forces, moments and power
         ## can be calculated by means of the blade element - momentum method (BEM)
         [Daxi,Mbetai,Mri,Pi,Cdaxi,Cpi,ai]=bem(V[i],thetai,betad,omri,xd,windturbine)
      Dax_list.append(Daxi)
      Mbeta_list.append(Mbetai)
      Mr_list.append(Mri)
      P_list.append(Pi)
      Cdax_list.append(Cdaxi)
      Cp_list.append(Cpi)
      a_list.append(ai)
      theta_list.append(thetai)
      omr_list.append(omri)
    return [Dax_list,Mbeta_list,Mr_list,P_list,Cdax_list,Cp_list,a_list,theta_list,omr_list]
