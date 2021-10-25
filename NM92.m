function [P1,P2,P3,P4]=NM92
% syntax: function [P1,P2,P3,P4]=NM92
% Input of all required parameters of the Vestas / NEG-Micon NM92 wind turbine
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
R=46;
% number of blades [-]
Nb=3;
% blade mass [kg]
mb=9700;
% inertia blade (with respect to flapping hinge) [kg m^2]
Jb=3.4e6;
% stifness flap spring [Nm/rad]
% the stiffness will be determined from the blade flap natural frequency omb [rad/s]
omb=4.5;
kb=Jb*omb^2;

% equivalent mass tower (1/4 mass tower + tower head mass) [kg]
mt=170000;
% stifness tower [N/m]
% the stiffness will be determined from the tower natural frequency [rad/s]
omt=2.45;
kt=mt*omt^2;
% damping tower [N/(m/s)]; 1% critical damping assumed
dt=2*0.01*sqrt(kt*mt);

% inertia generator [kg m^2]
Jg=210;
% nominal terminal (line-to-line) voltage generator [V]
Un=960;
% nominal generator power [W]
Pn=2.75e6;
% nominal generator shaft angular velocity [rad/s]
omgn=2*pi*25;
% field current generator [A]
If=80;
% number of pole pairs [-]
p=2;

% transmission ratio [-]
nu=71;
% inertia rotor [kg m^2]
Jr=Nb*Jb;
% stiffness transmission [Nm/rad]
kr=4.9e8;
% total inertia transmission [kg m^2]
Jtot=(nu^2*Jg*Jr)/(nu^2*Jg+Jr);
% damping transmission [Nm/(rad/s)]; 3% critical damping assumed
dr=2*0.03*sqrt(kr*Jtot);

% turbine parameters 
P2=[R,Nb,Jb,kb,mt,dt,kt,nu,Jr,dr,kr,Jg,Un,Pn,omgn,If,p];


% number of blade elements [-]
Ns=11;
% radial positions (with respect to rotor axis) of blade sections [m]; not necessary equidistant
% Note: the borders of the blade sections should be given; i.e. Ns+1 values
% first value is start of aerodynamic aerofoil; last value is blade tip (r=R)
r=[4  8  12  16  20  24  28  32  36  42  44  46];

% chord of blade sections [m] 
c=[2.6  3.0  3.2  2.8  2.4  2.1  1.8  1.6  1.3  0.73  0.46  0.05];

% twist of blade sections [degrees];
% by definition, the last value equals 0 (blade tip)
thetat=[6.695  9.37  9.39  5.42  3.499  2.31  1.281  0.559  -0.07  -1.17  -1.27  0];

% check
if (length(r) ~= Ns+1) error('number of radial positions not correct');end
if (length(c) ~= Ns+1) error('number of chord values not correct');end
if (length(thetat) ~= Ns+1) error('number of twist values not correct');end

% blade geometry
P3=[r;c;thetat];


% nominal wind speed [m/s]
Vn=11.5;
% nominal tip speed ratio [-]
lambdan=9.0;
% nominal blade pitch angle [degrees]
thetan=-0.3;

% nominal values
P4=[Vn,lambdan,thetan];