function [P1,P2,P3,P4]=V66
% syntax: function [P1,P2,P3,P4]=V66
% Input of all required parameters of the Vestas V66 wind turbine
% Outputs
%    aerodynamic parameters P1=[rho,kp]
%    turbine parameters P2=[R,Nb,Jb,kb,mt,dt,kt,nu,Jr,dr,kr,Jg,omg0,kg1,kg2]
%    blade geometry P3=[r;c;thetat]
%    nominal values P4=[Vn,lambdan,thetan]

% air density [kg/m3]
rho=1.25;
% power loss factor [-]; correction factor for the simplifications in BEM [-], see listing 'bem.m'
kp=0.9;

% aerodynamic parameters
P1=[rho,kp];


% rotor radius [m]
R=33;
% number of blades [-]
Nb=3;
% blade mass [kg]
mb=3500;
% inertia blade (with respect to flapping hinge) [kg m^2]
% assume a linear mass distribution
Jb=1/6*mb*R^2;
% stifness flap spring [Nm/rad]
% the stiffness will be determined from the blade flap natural frequency omb [rad/s]
omb=6;
kb=Jb*omb^2;

% mass tower (+ nacelle) [kg]
mt=180000;
% stifness tower [N/m]
% the stiffness will be determined from the tower natural frequency [rad/s]
omt=1.6;
kt=mt*omt^2;
% damping tower [N/(m/s)]; 1% critical damping assumed
dt=2*0.01*sqrt(kt*mt);

% inertia generator [kg m^2]
Jg=190;
% nominal terminal (line-to-line) voltage generator [V]
Un=690;
% nominal generator power [W]
Pn=2.2e6;
% nominal generator shaft angular velocity [rad/s]
omgn=2*pi*25;
% field current generator [A]
If=80;
% number of pole pairs [-]
p=2;

% transmission ratio [-]
nu=52;
% inertia rotor [kg m^2]
Jr=Nb*Jb;
% stiffness transmission [Nm/rad]
kr=1e8;
% total inertia transmission [kg m^2]
Jtot=(nu^2*Jg*Jr)/(nu^2*Jg+Jr);
% damping transmission [Nm/(rad/s)]; 3% critical damping assumed
dr=2*0.03*sqrt(kr*Jtot);

% turbine parameters 
P2=[R,Nb,Jb,kb,mt,dt,kt,nu,Jr,dr,kr,Jg,Un,Pn,omgn,If,p];


% number of blade elements [-]
Ns=10;
% radial positions (with respect to rotor axis) of blade sections [m]; not necessary equidistant
% Note: the borders of the blade sections should be given; i.e. Ns+1 values
% first value is start of aerodynamic aerofoil; last value is blade tip (r=R)
r=[3     6     9    12    15    18    21    24    27    30    33];
% chord of blade sections [m] 
c=[0   1.4   2.9   2.6   2.3   2.0   1.7   1.4   1.1   0.8   0.5];
% twist of blade sections [degrees];
% by definition, the last value equals 0 (blade tip)
thetat= ...
  [12.0  10.8  9.6  8.4   7.2   6.0   4.8   3.6   2.4   1.2   0.0];
% check
if (length(r) ~= Ns+1) error('number of radial positions not correct');end
if (length(c) ~= Ns+1) error('number of chord values not correct');end
if (length(thetat) ~= Ns+1) error('number of twist values not correct');end

% blade geometry
P3=[r;c;thetat];


% nominal wind speed [m/s]
Vn=13;
% nominal tip speed ratio [-]
lambdan=7.6;
% nominal blade pitch angle [degrees]
thetan=-2.4;

% nominal values
P4=[Vn,lambdan,thetan];
