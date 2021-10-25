
## written by Dennis van Dommelen, 2014

def gen(omg,windturbine):
    ## syntax: function [Mg,Pg]=gen(omg,windturbine)
    ## Ideal torque-rpm characteristic of a generator including converter
    ##
    ## Output:
    ##    Mg: generator torque [Nm]
    ##    Pg: generator power [W]
    ## Inputs:
    ##    omg: generator shaft angular velocity [rad/s]
    ##    windturbine name of file with wind turbine parameters
    ##                 e.g.: 'LW50'
    ##    Required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ##    P2: turbine parameters
    ##    P4: nominal values

    ## rotor radius [m]
    R=P2[0]
    ## transmission ratio [-]
    nu=P2[7]
    ## nominal (electrical) generator power [W]
    Pn=P2[12]
    ## efficiency generator [-]
    eta=P2[13]
    ## nominal wind speed [m/s]
    Vn=P4[0]
    ## nominal tip speed ratio [-]
    lambdan=P4[1]

    ## nominal generator shaft angular velocity [rad/s]
    omgn=nu*lambdan*Vn/R

    ## mechanical generator power (shaft power)
    ##  - at nominal speed: Psh=Pn/eta
    ##  - for constant lambda: Psh proportional to omg^3
    Psh=(omg/omgn)**3*Pn/eta
    ## generator torque
    Mg=Psh/omg

    ## electrical generator power
    Pg=eta*Psh

    return [Mg,Pg]
