import control.matlab as cm
from equi import equi
from gen import gen
from dynmod import dynmod

## written by Dennis van Dommelen, 2014

def transfer(windturbine,V0):
    ## syntax: sys=transfer(windturbine,V0)
    ## print sys
    ## Determination of the transfer function of the wind turbine
    ##
    ## Inputs:
    ##    windturbine: name of file with wind turbine parameters
    ##                 e.g.: 'LW50'
    ##    V0: undisturbed wind velocity [m/s]
    ## Outputs:
    ##    sys: the transfer function H(s) for all wind turbine inputs to all wind turbine outputs
    ##                   NUM(s)
    ##           H(s) = --------
    ##                   DEN(s)
    ##    inputs of wind turbine:
    ##      1) blade pitch angle theta [degrees]
    ##      2) undisturbed wind speed V [m/s]
    ##    outputs of wind turbine:
    ##      1) axial force Dax [N]
    ##      2) aerodynamic flap moment Mbeta [Nm]
    ##      3) aerodynamic rotor torque Mr [Nm]
    ##      4) generator power Pg [W]
    ##      5) blade pitch angle theta [degrees]
    ##      6) undisturbed wind speed V [m/s]
    ##    states of wind turbine:
    ##      1) flap angle beta [rad]
    ##      2) flap angular velocity betad [rad/s]
    ##      3) tower top displacement x [m]
    ##      4) tower top velocity xd [m/s]
    ##      5) rotor angular velocity omr [rad/s]
    ##      6) torsion angle transmission eps [rad]
    ##      7) torsion angular velocity transmission epsd [rad/s]


    ## constants with respect to the linearisation of the equations of motion
    ## minimum variation
    mindelta=1*10**(-7)
    ## relative variation
    reldelta=1*10**(-2)

    ## required parameters
    windturbine_name = windturbine+'.txt'
    [P1,P2,P3,P4]= eval(open(windturbine_name, 'r').read())
    ## stationary conditions: flap speed, tower top speed and torsion speed transmission equal zero
    betad=0
    xd=0
    epsd=0

    ## determination operating point (equilibrium state) of wind turbine for known V0
    [beta,x,omr,eps,omg,a,theta,Dax,Mbeta,Mr]=equi(windturbine,V0)
    ## generator power
    [Mg,Pg]=gen(omg,windturbine)

    ## initial state (stationary)
    X0=[beta,betad,x,xd,omr,eps,epsd]
    
    
    U0=[theta,V0]
    Y0=[Dax,Mbeta,Mr,Pg,theta,V0]

    ## numerical linearisation of the equations of motion (given in 'dynmod.m') into state space format:
    ##    XD = A X + B U
    ##     Y = C X + D U
    ##    with X states of the wind turbine: [beta;betad;x;xd;omr;eps;epsd]
    ##        XD time derivative of X
    ##        Y outputs of wind turbine: [Dax;Mbeta;Mr;Pg;theta;V]
    ##        U inputs of wind turbine: [theta;V]
    ## number of states
    NX=len(X0)
    ## number of outputs
    NY=len(Y0)

    
   
    
    A=[[0 for col in range(NX)] for row in range(NX)]
    C=[[0 for col in range(NX)] for row in range(NY)]
   
    ## variation around state X0
    for i in range(NX):
        delta=[0]*(len(X0))
        X1=[0]*len(X0)
        X2=[0]*len(X0)
        delta[i]=max(reldelta*X0[i],mindelta)
        for j in range(len(X0)):
           X1[j]=X0[j]+delta[j]
        [XD1,Y1]=dynmod(X1,U0,a,windturbine)
        for j in range(len(X0)):
           X2[j]=X0[j]-delta[j]
        [XD2,Y2]=dynmod(X2,U0,a,windturbine)
        for j in range(len(XD1)):
           A[j][i]=(XD1[j][0]-XD2[j][0])/(2*delta[i])
        for j in range(len(Y1)):
           C[j][i]=(Y1[j][0]-Y2[j][0])/(2*delta[i])
    

    ## number of inputs
    NU=len(U0)

    B=[[0 for col in range(NU)] for row in range(NX)]
    D=[[0 for col in range(NU)] for row in range(NY)]
    ## variation around input U0
    for i in range(NU):
        delta=[0]*(len(U0))
        U1=[0]*len(X0)
        U2=[0]*len(X0)
                   
        delta[i]=max(reldelta*U0[i],mindelta)
        for j in range(len(U0)):
           U1[j]=U0[j]+delta[j]
        [XD1,Y1]=dynmod(X0,U1,a,windturbine)
        for j in range(len(U0)):
           U2[j]=U0[j]-delta[j]
        [XD2,Y2]=dynmod(X0,U2,a,windturbine)
        for j in range(len(XD1)):
           B[j][i]=(XD1[j][0]-XD2[j][0])/(2*delta[i])
        for j in range(len(Y1)):               
           D[j][i]=(Y1[j][0]-Y2[j][0])/(2*delta[i])
    
    
    ## conversion from state space to transfer function
    sys=cm.ss(A,B,C,D)
    return sys
