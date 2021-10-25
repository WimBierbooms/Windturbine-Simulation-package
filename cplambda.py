from bem import bem

## written by Dennis van Dommelen, 2014

def cplambda(windturbine,lambdalist,theta):
    ## syntax: cplambda(windturbine,lambda,theta)
    ## Determination of the dimensionless characteristics:
    ##    thrust coefficient versus tip speed ratio       Cdax - lambda
    ##    power coefficient versus tip speed ratio        Cp - lambda
    ##    induction factor versus tip speed ratio         a - lambda
    ##
    ## Outputs:
    ##    Cdax: thrust coefficient [-]
    ##    Cp: power coefficient [-]
    ##    a: induction factor [-]
    ## Inputs:
    ##    windturbine: name of file with wind turbine parameters
    ##                 e.g.: 'LW50'
    ##    lambdalist: vector with tip speed ratios [-]
    ##    theta: blade pitch angle [degrees]

    ## required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ## rotor radius
    R=P2[0]

    ## stationary conditions: flap speed and tower top speed equal zero
    betad=0
    xd=0

    N=len(lambdalist)
    Cdax_list = []
    Cp_list = []
    a_list = []

    ## calculation of the aerodynamic coefficients for each tip speed ratio by means of blade element-momentum method (BEM)
    for i in range(N):
       ## arbitrary wind speed (Note: the dimensionless quantaties are independent of the wind speed)
       V=10.
       ## the rotor angular velocity is calculated on basis of the tip speed ratio
       omr=lambdalist[i]*V/R
       [Dax,Mbeta,Mr,P,Cdaxi,Cpi,ai]=bem(V,theta,betad,omr,xd,windturbine)
       Cdax_list.append(Cdaxi)
       Cp_list.append(Cpi)
       a_list.append(ai)
    return [Cdax_list,Cp_list,a_list]
    

