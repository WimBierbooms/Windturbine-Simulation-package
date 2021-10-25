from bem import bem

## written by Dennis van Dommelen, 2014

def powercurve2(windturbine,V,omr):
    ## syntax: powercurve2(windturbine,V,omr)
    ## Determination of the characteristics of a CONSTANT SPEED wind turbine
    ##    axial force versus wind speed                  Dax - V
    ##    aerodynamic flap moment versus wind speed      Mbeta - V
    ##    aerodynamic rotor torque versus wind speed     Mr - V
    ##    aerodynamic power versus wind speed            P - V
    ##    thrust coefficient versus wind speed           Cdax - V
    ##    power coefficient versus wind speed            Cp - V
    ##    induction factor versus wind speed             a - V
    ##
    ## Outputs:
    ##    Dax: axial force [N]
    ##    Mbeta: aerodynamic flap moment [Nm]
    ##    Mr: aerodynamic rotor torque [Nm]
    ##    P: aerodynamic power [W]
    ##    Cdax: thrust coefficient [-]
    ##    Cp: power coefficient [-]
    ##    a: induction factor [-]
    ## Inputs:
    ##    windturbine: name of file with wind turbine parameters
    ##                 e.g.: 'LW50'
    ##    V: vector with wind speeds [m/s]
    ##    omr: rotor angular velocity [rad/s]

    ## required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ## nominal blade pitch angle [degrees]
    thetan=P4[2]

    ## stationary conditions: flap speed and tower top speed equal zero
    betad=0.
    xd=0.

    N=len(V)

    ## the blade pitch angle equals nominal blade pitch angle
    theta=thetan

    ##creating empty lists for the results    
    Dax_list = []
    Mbeta_list = []
    Mr_list = []
    P_list = []
    Cdax_list = []
    Cp_list = []
    a_list = []
    ## calculation of the aerodynamic forces, moments etc., for each wind speed,
    ## by means of blade element-momentum method (BEM)
    for i in range(N):
        [Daxi,Mbetai,Mri,Pi,Cdaxi,Cpi,ai]=bem(V[i],theta,betad,omr,xd,windturbine)

        ##Add the entries to the lists
        Dax_list.append(Daxi)
        Mbeta_list.append(Mbetai)
        Mr_list.append(Mri)
        P_list.append(Pi)
        Cdax_list.append(Cdaxi)
        Cp_list.append(Cpi)
        a_list.append(ai)
    return [Dax_list,Mbeta_list,Mr_list,P_list,Cdax_list,Cp_list,a_list]

