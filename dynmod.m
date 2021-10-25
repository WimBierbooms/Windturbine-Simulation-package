function [XD,Y]=dynmod(X,U,a0,P1,P2,P3)
% syntax: function [XD,Y]=dynmod(X,U,a0,P1,P2,P3)
% Equations of motion of wind turbine (dynamic model):
% time derivatives of the states and outputs of the wind turbine as function of the states and inputs
%
% Outputs of the routine dynmod 
%   XD: time derivative of the states X
%       dbeta: flap angular velocity [rad/s]
%       ddbeta: flap angular acceleration [rad/s^2]
%       dx: tower top speed [m/s]
%       ddx: tower top acceleration [m/s^2]
%       domr: rotor angular acceleration [rad/s^2]
%       deps: torsion angular velocity transmission [rad/s]
%       ddeps: torsion angular acceleration transmission [rad/s^2]
%    Y: outputs of the wind turbine
%       Dax: axial force [N]
%       Mbeta: aerodynamic flap moment [Nm]
%       Mr: aerodynamic rotor torque [Nm]
%       Pg: generator power [W]
%       theta: blade pitch angle [degrees]
%       V: undisturbed wind speed [m/s]
% Inputs of the routine dynmod
%    X: states of the wind turbine
%       beta: flap angle [rad]
%       betad: flap angular velocity [rad/s]
%       x: tower top displacement [m]
%       xd: tower top velocity [m/s]
%       omr: rotor angular velocity [rad/s]
%       eps: torsion angle transmission [rad]
%       epsd: torsion angular velocity transmission [rad/s]
%    U: inputs of the wind turbine
%       theta: blade pitch angle [degrees]
%       V: undisturbed wind speed [m/s]
%    a0: induction factor [-]
%    P1: aerodynamic parameters
%    P2: turbine parameters
%    P3: blade geometry

% states
beta=X(1);
betad=X(2);
x=X(3);
xd=X(4);
omr=X(5);
eps=X(6);
epsd=X(7);

% inputs
theta=U(1);
V=U(2);


% rotor radius [m]
R=P2(1);
% number of blades [-]
Nb=P2(2);
% inertia blade (with respect to flapping hinge) [kg m^2]
Jb=P2(3);
% stifness flap spring [Nm/rad]
kb=P2(4);
% mass tower (+ nacelle) [kg]
mt=P2(5);
% damping tower [N/(m/s)]
dt=P2(6);
% stifness tower [N/m]
kt=P2(7);
% transmission ratio [-]
nu=P2(8);
% inertia rotor [kg m^2]
Jr=P2(9);
% damping transmission [Nm/(rad/s)]
dr=P2(10);
% stiffness transmission [Nm/rad]
kr=P2(11);
% inertia generator [kg m^2]
Jg=P2(12);
% nominal generator power [W]
Pn=P2(14);
% nominal generator shaft angular velocity [rad/s]
omgn=P2(15);

% total inertia transmission [kg m^2]
Jtot=(nu^2*Jg*Jr)/(nu^2*Jg+Jr);

% determination of the aerodynamic forces, moments and power
% the induction factor a is considered to be constant during the simulation ('frozen wake' assumption); so the
% blade element method can be applied instead of the blade element-momentum method (BEM)
[Dax,Mbeta,Mr,P,Cdax,Cp]=aero2(a0,V,theta,betad,omr,xd,P1,P2,P3);

% angular velocity generator equals difference rotor angular velocity
% and torsion angular velocity of transmission times transmission ratio
omg=nu*(omr-epsd);
% generator torque and power
[Mg,Pg,Ef,I1,V1,I2,eta]=gener(omg,(omg/omgn)^3*Pn,P2,690);

% equations of motion of turbine
% rotor blade with flap degree of freedom
dbeta=betad;
ddbeta=1/Jb*(Mbeta-(kb+Jb*omr^2)*beta);

% mass-spring-damper model tower
dx=xd;
ddx=1/mt*(Dax-dt*xd-kt*x);

% the transmission consists out of 2 rotational inertia's (rotor and
% generator resp.) connected with a rotational damper and stiffness
domr=1/Jr*(Mr-dr*epsd-kr*eps);
deps=epsd;
ddeps=1/Jtot*(Jtot/Jr*Mr+Jtot/(nu^2*Jg)*nu*Mg-dr*epsd-kr*eps);

% time derivatives of the states
XD(1)=dbeta;
XD(2)=ddbeta;
XD(3)=dx;
XD(4)=ddx;
XD(5)=domr;
XD(6)=deps;
XD(7)=ddeps;
% conversion from row to column vector
XD=XD';

% outputs
Y(1)=Dax;
Y(2)=Mbeta;
Y(3)=Mr;
Y(4)=Pg;
Y(5)=theta;
Y(6)=V;
% conversion from row to column vector
Y=Y';
