import numpy as np

## written by Dennis van Dommelen, 2014

document = open('NREL_5MW.txt', 'w')
## syntax: NREL_5MW()
## Input of all required parameters of the NREL 5MW wind turbine
## Outputs
##    aerodynamic parameters P1=[rho,kp]
##    turbine parameters P2=[R,Nb,Jb,kb,mt,dt,kt,nu,Jr,dr,kr,Jg,Pn,eta]
##    blade geometry P3=[r,c,thetat]
##    nominal values P4=[Vn,lambdan,thetan]

## air density [kg/m3]
rho=1.25
## power loss factor [-]; correction factor for the simplifications in BEM [-], see listing 'bem.m'
kp=0.9

## aerodynamic parameters
P1=[rho,kp]

## rotor radius [m]
R=63.
## number of blades [-]
Nb=3.
## blade mass [kg]
mb=17740.
## inertia blade (with respect to flapping hinge) [kg m^2]
Jb=11776047.
## stifness flap spring [Nm/rad]
## the stiffness will be determined from the blade flap natural frequency omb [rad/s]
omb=.668*2*np.pi
kb=Jb*omb**2

## mass tower + nacelle [kg]
mt=347460.+240000.
## the stiffness will be determined from the tower natural frequency [rad/s]
omt=0.32*2*np.pi
kt=mt*omt**2
## damping tower [N/(m/s)]; 1## critical damping assumed
dt=2.*0.01*np.sqrt(kt*mt)

## inertia generator [kg m^2]
Jg=534.116
## nominal (electrical) generator power [W]
Pn=4766949.
## efficiency generator [-]
eta=0.9

## transmission ratio [-]
nu=97.
## inertia rotor [kg m^2]
Jr=Nb*Jb
## stiffness transmission [Nm/rad]
kr=867637000.
## total inertia transmission [kg m^2]
Jtot=(nu**2*Jg*Jr)/(nu**2*Jg+Jr)
## damping transmission [Nm/(rad/s)]; 5## critical damping assumed
dr=2.*0.05*np.sqrt(kr*Jtot)

## turbine parameters 
P2=[R,Nb,Jb,kb,mt,dt,kt,nu,Jr,dr,kr,Jg,Pn,eta]

## number of blade elements [-]
Ns=14.
## radial positions (with respect to rotor axis) of blade sections [m]; not necessary equidistant
## Note: the borders of the blade sections should be given; i.e. Ns+1 values
## first value is start of aerodynamic aerofoil; last value is blade tip (r=R)
r=[9.70, 13.80, 17.90, 22.00, 26.10, 30.20, 34.30, 38.40, 42.50, 46.60, 50.70, 54.80, 57.5333, 60.2667, 63.00]

## chord of blade sections [m] 
c=[4.348, 4.625, 4.580, 4.356, 4.131, 3.878, 3.624, 3.379, 3.133, 2.887, 2.641, 2.400, 2.218, 1.821, 0.961]

## twist of blade sections [degrees];
## by definition, the last value equals 0 (blade tip)
thetat= [13.308, 12.38, 10.76, 9.596, 8.408, 7.167, 5.952, 4.761, 3.638, 2.697, 1.926, 1.131, 0.593, 0.215, 0.0]

## check
if (len(r) != Ns+1):
    print 'number of radial positions not correct'
if (len(c) != Ns+1):
    print 'number of chord values not correct'
if (len(thetat) != Ns+1):
    print 'number of twist values not correct'

## blade geometry
P3=[r,c,thetat]

## nominal (rated) wind speed [m/s]
Vn=11.4
## nominal (rated) tip speed ratio [-]
lambdan=7.3
## nominal (rated) blade pitch angle [degrees]
thetan=-1.5

## nominal values
P4=[Vn,lambdan,thetan]

text=str(P1)+','+str(P2)+','+str(P3)+','+str(P4)
document.write(text)
document.close()

