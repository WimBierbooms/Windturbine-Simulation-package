function [P1,P2,P3,P4]=LW50
% syntax: function [P1,P2,P3,P4]=LW50
% Input of all required parameters of the Lagerwey LW 50/750 wind turbine
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
R=25;
% number of blades [-]
Nb=3;
% inertia blade (with respect to flapping hinge) [kg m^2]
Jb=3e5;
% stifness flap spring [Nm/rad]
kb=4e7;

% mass tower (+ nacelle) [kg]
mt=60000;
% stifness tower [N/m]
kt=5e5;
% damping tower [N/(m/s)]; 1% critical damping assumed
dt=2*0.01*sqrt(kt*mt);

% inertia generator [kg m^2]
Jg=140;
% nominal terminal (line-to-line) voltage generator [V]
Un=690;
% nominal generator power [W]
Pn=0.77e6;
% nominal generator shaft angular velocity [rad/s]
omgn=2*pi*50/95;
% field current generator [A]
If=30;
% number of pole pairs [-]
p=95;

% transmission ratio [-]
nu=1;
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
Ns=9;
% radial positions (with respect to rotor axis) of blade sections [m]; not necessary equidistant
% Note: the borders of the blade sections should be given; i.e. Ns+1 values
% first value is start of aerodynamic aerofoil; last value is blade tip (r=R)
r=[ 7.00 9.00 11.00 13.00 15.00 17.00 19.00 21.00 23.00 25.00];
% chord of blade sections [m] 
c=[ 2.10 1.95  1.72  1.52  1.35  1.18  1.03  0.89  0.75  0.49];
% twist of blade sections [degrees];
% by definition, the last value equals 0 (blade tip)
thetat= ...
  [12.00 8.72  6.50  4.84  3.47  2.29  1.29  0.54  0.10  0.00];
% check
if (length(r) ~= Ns+1) error('number of radial positions not correct');end
if (length(c) ~= Ns+1) error('number of chord values not correct');end
if (length(thetat) ~= Ns+1) error('number of twist values not correct');end

% blade geometry
P3=[r;c;thetat];


% nominal wind speed [m/s]
Vn=11;
% nominal tip speed ratio [-]
lambdan=7.5;
% nominal blade pitch angle [degrees]
thetan=-0.5;

% nominal values
P4=[Vn,lambdan,thetan];
