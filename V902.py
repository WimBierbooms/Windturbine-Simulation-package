import numpy as np

## written by Dennis van Dommelen, 2014

document = open('V902.txt', 'w')
## syntax: V90
## Input of all required parameters of the Vestas V90 wind turbine
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
R=45.
## number of blades [-]
Nb=3.
## blade mass [kg]
mb=9600.
## inertia blade (with respect to flapping hinge) [kg m^2]
Jb=3.9*10**6
## stifness flap spring [Nm/rad]
## the stiffness will be determined from the blade flap natural frequency omb [rad/s]
omb=5.75
kb=Jb*omb**2

## equivalent mass tower (1/4 mass tower + tower head mass) [kg]
mt=160000.
## stifness tower [N/m]
## the stiffness will be determined from the tower natural frequency [rad/s]
omt=8.*7.8/45.
kt=mt*omt**2
## damping tower [N/(m/s)]; 1## critical damping assumed
dt=2*0.01*np.sqrt(kt*mt)

## inertia generator [kg m^2]
Jg=60.
## nominal (electrical) generator power [W]
Pn=3*10**6
## efficiency generator [-]
eta=0.9

## transmission ratio [-]
nu=98.
## inertia rotor [kg m^2]
Jr=Nb*Jb
## stiffness transmission [Nm/rad]
kr=1.8*10**8
## total inertia transmission [kg m^2]
Jtot=(nu**2*Jg*Jr)/(nu**2*Jg+Jr)
## damping transmission [Nm/(rad/s)]; 3## critical damping assumed
dr=2*0.03*np.sqrt(kr*Jtot)

## turbine parameters 
P2=[R,Nb,Jb,kb,mt,dt,kt,nu,Jr,dr,kr,Jg,Pn,eta]


## number of blade elements [-]
Ns=6
## radial positions (with respect to rotor axis) of blade sections [m]; not necessary equidistant
## Note: the borders of the blade sections should be given; i.e. Ns+1 values
## first value is start of aerodynamic aerofoil; last value is blade tip (r=R)
r=[4,  6.6,  10.6,	18.5,  30.4,  41,  45]
## chord of blade sections [m] 
c=[3.1,  3.9,  3.9,  3.1,  2.1,  1.3,  0.03]

## twist of blade sections [degrees];
## by definition, the last value equals 0 (blade tip)
thetat=[13,  13,  11,  7.8,  3.3,  0.3,  0]

## check
if (len(r) != Ns+1):
    print 'number of radial positions not correct'
if (len(c) != Ns+1):
    print 'number of chord values not correct'
if (len(thetat) != Ns+1):
    print 'number of twist values not correct'

## blade geometry
P3=[r,c,thetat]


## nominal wind speed [m/s]
Vn=12.0
## nominal tip speed ratio [-]
lambdan=7.8
## nominal blade pitch angle [degrees]
thetan=-1.5

## nominal values
P4=[Vn,lambdan,thetan]

text=str(P1)+','+str(P2)+','+str(P3)+','+str(P4)
document.write(text)
document.close()

