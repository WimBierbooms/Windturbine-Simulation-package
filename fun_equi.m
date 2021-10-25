function Md=fun_equi(omr,V,theta,P1,P2,P3)
% syntax: function Md=fun_equi(omr,V,theta,P1,P2,P3)
% Determination of difference between aerodynamic rotor torque and generator torque,
% for known rotor angular velocity
% This function is used by 'equi.m'
%
% Output:
%    Md: difference in torque [Nm]
% Inputs:
%    omr: rotor angular velocity [rad/s]
%    V: undisturbed wind speed [m/s]
%    theta: pitch angle [degrees]
%    P1: aerodynamic parameters
%    P2: turbine parameters
%    P3: blade geometry

% required parameters
% transmission ratio [-]
nu=P2(8);
% nominal generator power [W]
Pn=P2(14);
% nominal generator shaft angular velocity [rad/s]
omgn=P2(15);

% stationary conditions: flap velocity and tower top velocity are equal zero
betad=0;
xd=0;

% aerodynamic rotor torque Mr according to blade element-momentum methode (BEM) for known rotor angular velocity
[Dax,Mbeta,Mr,P,Cdax,Cp,a]=bem(V,theta,betad,omr,xd,P1,P2,P3);

% stationary generator angular velocity (for known rotor angular velocity)
omg=nu*omr;
% generator torque (from function 'gener.m')
[Mg,Pg,Ef,I1,V1,I2,eta]=gener(omg,(omg/omgn)^3*Pn,P2,690);
% generator torque, with respect to the low speed shaft
Mg2=nu*Mg;

% difference in torque (with respect to the low speed shaft)
Md=Mr-Mg2;
