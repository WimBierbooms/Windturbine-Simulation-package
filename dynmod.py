from aero import aero
from gen import gen

## written by Dennis van Dommelen, 2014

def dynmod(X,U,a0,windturbine):

    ## syntax: dynmod(X,U,a0,windturbine)
    ## Equations of motion of wind turbine (dynamic model):
    ## time derivatives of the states and outputs of the wind turbine as function of the states and inputs
    ##
    ## Outputs of the routine dynmod 
    ##   XD: time derivative of the states X
    ##       dbeta: flap angular velocity [rad/s]
    ##       ddbeta: flap angular acceleration [rad/s^2]
    ##       dx: tower top speed [m/s]
    ##       ddx: tower top acceleration [m/s^2]
    ##       domr: rotor angular acceleration [rad/s^2]
    ##       deps: torsion angular velocity transmission [rad/s]
    ##       ddeps: torsion angular acceleration transmission [rad/s^2]
    ##    Y: outputs of the wind turbine
    ##       Dax: axial force [N]
    ##       Mbeta: aerodynamic flap moment [Nm]
    ##       Mr: aerodynamic rotor torque [Nm]
    ##       Pg: generator power [W]
    ##       theta: blade pitch angle [degrees]
    ##       V: undisturbed wind speed [m/s]
    ## Inputs of the routine dynmod
    ##    X: states of the wind turbine
    ##       beta: flap angle [rad]
    ##       betad: flap angular velocity [rad/s]
    ##       x: tower top displacement [m]
    ##       xd: tower top velocity [m/s]
    ##       omr: rotor angular velocity [rad/s]
    ##       eps: torsion angle transmission [rad]
    ##       epsd: torsion angular velocity transmission [rad/s]
    ##    U: inputs of the wind turbine
    ##       theta: blade pitch angle [degrees]
    ##       V: undisturbed wind speed [m/s]
    ##    a0: induction factor [-]
    ##    windturbine name of file with wind turbine parameters
    ##                 e.g.: 'LW50'

    ##    required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    
    ##    P1: aerodynamic parameters
    ##    P2: turbine parameters
    ##    P3: blade geometry
    ##    P4: nominal values


    ## states
    beta=X[0]
    betad=X[1]
    x=X[2]
    xd=X[3]
    omr=X[4]
    eps=X[5]
    epsd=X[6]

    ## inputs
    theta=U[0]
    V=U[1]

    ## inertia blade (with respect to flapping hinge) [kg m^2]
    Jb=P2[2]
    ## stifness flap spring [Nm/rad]
    kb=P2[3]
    ## mass tower (+ nacelle) [kg]
    mt=P2[4]
    ## damping tower [N/(m/s)]
    dt=P2[5]
    ## stifness tower [N/m]
    kt=P2[6]
    ## transmission ratio [-]
    nu=P2[7]
    ## inertia rotor [kg m^2]
    Jr=P2[8]
    ## damping transmission [Nm/(rad/s)]
    dr=P2[9]
    ## stiffness transmission [Nm/rad]
    kr=P2[10]
    ## inertia generator [kg m^2]
    Jg=P2[11]

    ## total inertia transmission [kg m^2]
    Jtot=(nu**2*Jg*Jr)/(nu**2*Jg+Jr)

    ## determination of the aerodynamic forces, moments and power
    ## the induction factor a is considered to be constant during the simulation ('frozen wake' assumption); so the
    ## blade element method can be applied instead of the blade element-momentum method (BEM)
    [Dax,Mbeta,Mr,P,Cdax,Cp]=aero(a0,V,theta,betad,omr,xd,windturbine)

    ## angular velocity generator equals difference rotor angular velocity
    ## and torsion angular velocity of transmission times transmission ratio
    omg=nu*(omr-epsd)
    ## generator torque and power
    [Mg,Pg]=gen(omg,windturbine)

    ## equations of motion of turbine
    ## rotor blade with flap degree of freedom
    dbeta=betad
    ddbeta=1/Jb*(Mbeta-(kb+Jb*omr**2)*beta)

    ## mass-spring-damper model tower
    dx=xd
    ddx=1/mt*(Dax-dt*xd-kt*x)

    ## the transmission consists out of 2 rotational inertia's (rotor and
    ## generator resp.) connected with a rotational damper and stiffness
    domr=1/Jr*(Mr-dr*epsd-kr*eps)
    deps=epsd
    ddeps=1/Jtot*(Jtot/Jr*Mr+Jtot/(nu**2*Jg)*nu*Mg-dr*epsd-kr*eps)

    ##generate empty vector XD
    XD = []
    ## time derivatives of the states
    XD.append(dbeta)
    XD.append(ddbeta)
    XD.append(dx)
    XD.append(ddx)
    XD.append(domr)
    XD.append(deps)
    XD.append(ddeps)
    ## conversion from row to column vector
    XD=zip(XD)

    ##generate empty vector Y
    Y=[]
    ## outputs
    Y.append(Dax)
    Y.append(Mbeta)
    Y.append(Mr)
    Y.append(Pg)
    Y.append(theta)
    Y.append(V)
    ## conversion from row to column vector
    Y=zip(Y)

    return [XD,Y]


